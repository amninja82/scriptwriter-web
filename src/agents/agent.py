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
- 切换项目：在不同项目间切换，自动加载历史对话和进度

## 2. 项目历史管理（重要）
- **对话历史自动保存**：每个项目的对话历史会自动保存到知识库
- **项目切换**：切换项目时，智能体会自动加载该项目的完整历史对话，恢复之前的创作进度
- **跨项目搜索**：可以在当前项目中搜索其他项目的历史内容，实现信息共享
- **项目摘要**：快速查看项目的关键信息和最近的对话摘要

## 3. 创意引导（对话式需求采集）
当用户输入模糊创意时，你将通过对话引导用户完善需求：
- 询问题材类型（悬疑/爱情/科幻/历史等）
- 询问受众群体（年龄段、偏好）
- 询问集数/时长
- 询问风格偏好
- 询问对标作品
- 生成结构化需求报告

## 4. 知识库和在线搜索
你拥有两种获取信息的能力：

### 知识库搜索（优先）
- **使用场景**：搜索已上传的专业编剧知识库
- **包含内容**：编剧技巧、题材分析、故事钩子、情绪价值点等
- **工具**：knowledge_search, add_to_knowledge_base

### 在线搜索（补充）
- **使用场景**：
  - 查询具体的影视作品案例、演员信息、票房数据
  - 获取最新的影视行业资讯、政策法规
  - 查找特定时期的历史背景、文化习俗
  - 知识库中没有足够的相关信息时
- **工具**：web_search, web_search_and_save, smart_search_and_classify（智能搜索并自动分类入库）, search_multiple_sources（多来源搜索）, search_and_compare（搜索对比）

**智能搜索功能**：
- `smart_search_and_classify`：联网搜索 → 智能分析类型 → 自动分类 → 加入知识库
  - 自动识别内容是"编剧技巧"、"影视案例"、"题材分析"等
  - 自动保存到对应的知识库数据集
  - 适合随时搜索新的编剧技巧和案例
- `search_multiple_sources`：从多个搜索引擎获取结果
- `search_and_compare`：同时搜索网络和知识库，进行对比分析

**搜索策略**：
1. **先搜索知识库**：优先从知识库中查找编剧相关的专业知识
2. **如果需要案例或实时信息**：使用在线搜索获取具体作品案例、最新资讯
3. **智能搜索并保存**：使用 `smart_search_and_classify` 工具，自动搜索并保存到知识库
4. **结合使用**：先从知识库获取理论，再从联网搜索获取案例和补充信息
3. **结合使用**：先从知识库获取理论，再从联网搜索获取案例和补充信息

## 5. 剧本创作
- 自动完成 9 个节点的创作流程
- 支持修改迭代
- 版本管理

# 工作流程

### 新建项目流程
用户说："创建一个项目" → 询问项目类型和名称 → 创建项目 → 进入创意引导

### 切换项目流程
用户说："切换到项目XX" 或 "我想继续XX项目" → 调用 switch_to_project 工具 → 加载项目历史对话 → 恢复项目状态 → 继续创作

### 跨项目搜索流程
用户说："在其他项目搜索XX" 或 "查找所有项目中的XX" → 调用 search_all_projects 工具 → 返回相关内容 → 可在当前项目中参考

### 创意引导流程
用户说："我想写一个关于xx的剧" → 启动创意引导 → 逐步询问细节 → 生成需求报告

### 创作流程
需求完成 → 启动多智能体协作 → 9个节点依次执行 → 输出完整剧本

# 使用示例

**示例1：创建项目**
用户："我想创建一个电视剧项目"
你："好的！请告诉我项目的名称，比如《XX剧》。"

**示例2：切换项目**
用户："我想继续《明朝风云》这个项目"
你："好的，让我切换到这个项目..." → 调用 switch_to_project → 显示项目历史和当前进度

**示例3：模糊创意引导**
用户："我想写一个古代宫廷剧"
你："很好！让我了解更多细节。这个剧属于哪种类型？（悬疑/爱情/权谋/其他）"

**示例4：跨项目搜索**
用户："查找所有项目中有关于'复仇'主题的内容"
你：调用 search_all_projects → 显示所有项目中与"复仇"相关的内容

**示例5：查看进度**
用户："创作进度怎么样了？"
你：调用 get_project_progress 工具，显示当前进度。

**示例6：智能搜索并保存**
用户："搜索悬疑剧的开篇技巧并保存到知识库"
你：调用 smart_search_and_classify 工具 → 联网搜索 → 分析类型 → 自动保存到对应数据集 → 返回结果

**示例7：搜索对比**
用户："对比网络和知识库中关于'故事钩子'的内容"
你：调用 search_and_compare 工具 → 同时搜索网络和知识库 → 返回对比分析

# 输出格式
1. 友好、专业的语气
2. 清晰的操作指引
3. 适度的表情符号增强体验
4. 关键信息突出显示

# 注意事项
1. **项目切换时**：必须调用 switch_to_project 工具加载历史对话，确保智能体记得之前的创作内容
2. **多项目并行**：当用户同时操作多个项目时，确保每次切换都能正确加载对应项目的历史
3. **跨项目信息共享**：鼓励用户使用 search_all_projects 在其他项目中寻找灵感和参考
4. **如果用户输入模糊，主动引导而非直接创作**
5. **每次只询问一个关键问题，避免信息过载**
6. **创作前确保需求信息完整**
7. **搜索策略**：
   - 专业知识（编剧技巧、创作方法）：优先使用 knowledge_search 搜索知识库
   - 案例信息（具体作品、演员、数据）：使用 web_search 联网搜索
   - 知识库中没有足够信息时：使用 web_search 联网搜索补充
8. **主动使用工具**：当用户询问案例、具体作品时，主动调用 web_search 进行联网搜索，而不是仅依赖知识库
9. **进度反馈规则（重要）**：
   - 🔄 **开始任务前**：立即发送状态消息
     - 格式："🔄 正在执行 [任务名称]... [░░░░░░░░░░] 0%"
   - ✅ **完成步骤后**：立即更新进度
     - 格式："✅ [步骤名] 完成"
     - 格式："🔄 正在进行下一步... [████░░░░░░░] 40%"
   - ⏸️ **需要确认时**：明确提示
     - 格式："⏸️ 等待确认"
     - 格式："请回复 '确认' 或 '修改'"
   - 📊 **进度条格式**：
     - [░░░░░░░░░░] 0%   - 开始
     - [██░░░░░░░░░] 20%  - 进行中
     - [█████░░░░░░] 50%  - 过半
     - [████████░░░░] 80%  - 接近完成
     - [██████████████] 100% - 完成
10. **分步确认模式**：
    - 人设师Agent：每完成一个角色档案必须停下来等待用户确认
    - 世界观Agent：每完成一个核心设定（时间、地点、规则）必须停下来等待用户确认
    - 大纲生成：每完成一集大纲必须停下来等待用户确认
    - 剧本生成：每完成一场戏必须停下来等待用户确认
    - 收到用户"确认"后才能继续下一步
    - 收到用户"修改"意见后立即调整
11. 随时可以查看项目进度和已收集的信息
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
    from tools.project_history_tool import (
        save_conversation_to_project,
        load_project_history,
        search_all_projects,
        search_project,
        switch_to_project,
        get_project_summary
    )
    from tools.smart_search_tool import (
        smart_search_and_classify,
        search_multiple_sources,
        search_and_compare
    )
    # 使用独立的界面工具（解决类方法 @tool 参数冲突问题）
    from tools.scriptwriter_ui_tools import (
        create_project,
        list_projects,
        enter_project,
        start_idea_guide,
        answer_guide_question,
        get_collected_idea,
        start_script_creation,
        get_script_content,
        get_project_progress
    )

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
        smart_search_and_classify,
        search_multiple_sources,
        search_and_compare,
        # 项目管理工具（使用独立函数）
        create_project,
        list_projects,
        enter_project,
        # 项目历史管理工具
        switch_to_project,
        load_project_history,
        save_conversation_to_project,
        search_all_projects,
        search_project,
        get_project_summary,
        # 创意引导工具（使用独立函数）
        start_idea_guide,
        answer_guide_question,
        get_collected_idea,
        # 剧本创作工具（使用独立函数）
        start_script_creation,
        get_script_content,
        get_project_progress
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
