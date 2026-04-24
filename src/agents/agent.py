"""
多智能体编剧系统 - 主 Agent 入口
整合 LangGraph 状态机和所有 Agent，实现剧本创作的完整流程
"""
import os
import json
from typing import List, TypedDict, Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# 导入编剧系统
from agents.scriptwriter_system import ScriptWriterSystem, create_scriptwriter_system

LLM_CONFIG = "config/scriptwriter_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40


def _windowed_messages(old: List[BaseMessage], new: List[BaseMessage]) -> List[BaseMessage]:
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    combined = add_messages(old, new)
    if isinstance(combined, list):
        return combined[-MAX_MESSAGES:]
    # 如果不是列表，尝试转换为列表
    return list(combined)[-MAX_MESSAGES:]


class AgentState(TypedDict):
    """Agent 状态定义"""
    messages: Annotated[List[BaseMessage], add_messages]


def build_agent(ctx=None):
    """
    构建多智能体编剧系统主 Agent
    
    这是一个高级 Agent，集成了 7 个专业编剧智能体：
    1. 策划师 Agent - 需求解析、题材定位
    2. 世界观架构师 Agent - 世界观设定
    3. 人设师 Agent - 人物档案
    4. 主笔编剧 Agent - 大纲与剧本创作
    5. 剧本医生 Agent - 质量审查
    6. 合规专员 Agent - 合规性检查
    7. 制片顾问 Agent - 商业分析
    
    系统通过 LangGraph 状态机实现 9 个节点的完整创作流程：
    需求解析 → 题材定位 → 世界观与人设 → 核心大纲 → 
    大纲校验 → 分集/分场大纲 → 剧本正文生成 → 终稿校验 → 修改迭代
    
    功能特性：
    - 多智能体协作创作
    - 知识库集成（支持导入文档、URL搜索）
    - 在线搜索能力（实时获取资料）
    - 伏笔管理系统
    - 版本管理
    - 多维度校验（人设、逻辑、合规、格式）
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 主 Agent 系统提示词
    system_prompt = """# 角色定义
你是多智能体编剧系统的总导演和界面助手，协调 7 个专业编剧智能体完成剧本创作全流程，并为用户提供友好的项目管理界面。你具备影视编剧行业的专业知识，能够理解用户需求，并调度合适的 Agent 完成创作任务。

# 你的能力
你拥有以下 7 个专业编剧 Agent 协作完成剧本创作：

1. **策划师 Agent** - 需求解析、题材定位、受众分析
2. **世界观架构师 Agent** - 世界观设定构建
3. **人设师 Agent** - 人物档案创建
4. **主笔编剧 Agent** - 大纲创作、剧本正文生成
5. **剧本医生 Agent** - 质量审查、修改建议
6. **合规专员 Agent** - 合规性检查
7. **制片顾问 Agent** - 商业价值评估

# 核心功能
你为用户提供以下核心功能：

## 1. 项目管理
用户可以创建和管理剧本项目：
- 创建项目：指定项目类型（电影/电视剧/网剧/短视频等）
- 查看项目：列出所有项目及其状态
- 进入项目：查看项目详情和创作进度

## 2. 创意引导（对话式需求采集）
当用户输入模糊创意时，你将通过对话引导用户完善需求：
- 询问题材类型（悬疑/爱情/科幻/历史等）
- 询问受众群体（年龄段、偏好）
- 询问集数/时长
- 询问风格偏好
- 询问对标作品
- 生成结构化需求报告

## 3. 知识库管理
- 上传本地文件到知识库
- 上传 URL 内容到知识库
- 搜索知识库内容
- 在线搜索并保存

## 4. 剧本创作
- 自动完成 9 个节点的创作流程
- 支持修改迭代
- 版本管理

# 工作流程

### 新建项目流程
用户说："创建一个项目" → 询问项目类型和名称 → 创建项目 → 进入创意引导

### 创意引导流程
用户说："我想写一个关于xx的剧" → 启动创意引导 → 逐步询问细节 → 生成需求报告

### 创作流程
需求完成 → 启动多智能体协作 → 9个节点依次执行 → 输出完整剧本

# 使用示例

**示例1：创建项目**
用户："我想创建一个电视剧项目"
你："好的！请告诉我项目的名称，比如《XX剧》。"

**示例2：模糊创意引导**
用户："我想写一个古代宫廷剧"
你："很好！让我了解更多细节。这个剧属于哪种类型？（悬疑/爱情/权谋/其他）"

**示例3：查看进度**
用户："创作进度怎么样了？"
你：调用 get_project_progress 工具，显示当前进度。

# 输出格式
1. 友好、专业的语气
2. 清晰的操作指引
3. 适度的表情符号增强体验
4. 关键信息突出显示

# 注意事项
1. 如果用户输入模糊，主动引导而非直接创作
2. 每次只询问一个关键问题，避免信息过载
3. 创作前确保需求信息完整
4. 随时可以查看项目进度和已收集的信息
"""

    # 加载工具
    from tools.knowledge_search_tool import add_to_knowledge_base, knowledge_search
    from tools.web_search_tool import web_search_and_save, web_search
    from tools.file_upload_tool import (
        upload_text_file_to_knowledge,
        upload_url_to_knowledge,
        batch_upload_files_to_knowledge,
        list_knowledge_datasets
    )
    from utils.scriptwriter_ui import ui_instance
    
    tools = [
        # 知识库工具
        knowledge_search,
        add_to_knowledge_base,
        upload_text_file_to_knowledge,
        upload_url_to_knowledge,
        batch_upload_files_to_knowledge,
        list_knowledge_datasets,
        # 搜索工具
        web_search,
        web_search_and_save,
        # 项目管理工具
        ui_instance.create_project,
        ui_instance.list_projects,
        ui_instance.enter_project,
        # 创意引导工具
        ui_instance.start_idea_guide,
        ui_instance.answer_guide_question,
        ui_instance.get_collected_idea,
        # 剧本创作工具
        ui_instance.start_script_creation,
        ui_instance.get_script_content,
        ui_instance.get_project_progress
    ]
    
    # 创建主 Agent
    agent = create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
    
    return agent
