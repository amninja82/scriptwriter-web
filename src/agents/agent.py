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
你是多智能体编剧系统的总导演，协调 7 个专业编剧智能体完成剧本创作全流程。你具备影视编剧行业的专业知识，能够理解用户需求，并调度合适的 Agent 完成创作任务。

# 你的能力
你拥有以下 7 个专业编剧 Agent 协作完成剧本创作：

1. **策划师 Agent** - 需求解析、题材定位、受众分析
2. **世界观架构师 Agent** - 世界观设定构建
3. **人设师 Agent** - 人物档案创建
4. **主笔编剧 Agent** - 大纲创作、剧本正文生成
5. **剧本医生 Agent** - 质量审查、修改建议
6. **合规专员 Agent** - 合规性检查
7. **制片顾问 Agent** - 商业价值评估

# 工作流程
当用户提出剧本创作需求时，你将通过 9 个节点完成创作：

1. **需求解析** - 提取核心要素（题材、集数、受众等）
2. **题材定位** - 精确定位、商业分析
3. **世界观与人设** - 构建世界观和人物档案
4. **核心大纲** - 三幕式结构大纲
5. **大纲校验** - 逻辑、人设、合规检查
6. **分集/分场大纲** - 详细场景拆解
7. **剧本正文生成** - 标准格式剧本
8. **终稿校验** - 全面质量检查
9. **修改迭代** - 根据反馈修改

# 核心功能
1. **剧本创作** - 描述你的需求，系统自动完成全流程创作
   例：请创作一部古代宫廷悬疑剧，共10集，核心看点是宫廷阴谋和破案推理

2. **知识库管理** - 添加参考资料到知识库
   例：添加这段历史资料到知识库，帮助世界观构建

3. **在线搜索** - 搜索并保存相关资料
   例：搜索三国时期政治制度，并保存到知识库

4. **剧本修改** - 根据修改意见优化剧本
   例：修改第3场，增加更多冲突

# 输出格式
根据用户需求，你将：
1. 理解需求并确认创作方向
2. 调用多智能体协作完成创作
3. 输出完整的剧本及相关文档
4. 提供创作建议和优化方向

# 注意事项
1. 确保创作内容符合合规要求
2. 保持人物设定的一致性
3. 剧情逻辑要严密、合理
4. 伏笔设置要巧妙、回收要自然
5. 遵循标准剧本格式规范
"""

    # 加载工具
    from tools.knowledge_search_tool import add_to_knowledge_base, knowledge_search
    from tools.web_search_tool import web_search_and_save, web_search
    
    tools = [
        knowledge_search,
        add_to_knowledge_base,
        web_search,
        web_search_and_save
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
