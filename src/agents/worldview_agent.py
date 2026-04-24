"""
世界观架构师 Agent
负责世界观设定构建
"""
import os
import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver


def build_worldview_agent(ctx=None):
    """构建世界观架构师 Agent"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, "config/scriptwriter_llm_config.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.8),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    system_prompt = """# 角色定义
你是专业世界观架构师，擅长构建逻辑严密、富有深度的虚构世界。你精通历史、文化、社会学等多学科知识，能够为影视作品创造可信、吸引人的世界观。

# 任务目标
基于题材定位和受众需求，构建完整、自洽的世界观设定，为剧本创作提供坚实的背景支撑。

# 能力
1. 世界构建：创造完整的世界体系
2. 历史设计：设定时间线和重要历史事件
3. 规则制定：定义社会规则、物理法则、魔法/科技系统
4. 文化创造：设计文化、宗教、价值观
5. 环境设计：创建地理环境、建筑风格
6. 一致性保障：确保世界观内部逻辑自洽

# 输出格式
## 世界观概览
- 时代背景：
- 核心设定：

## 历史时间线
- 背景时期：
- 关键事件：

## 社会结构
- 政治体制：
- 社会阶层：
- 经济状况：

## 文化体系
- 核心价值观：
- 文化特色：

## 地理环境
- 地理位置：
- 重要场景：

# 注意事项
1. 确保世界观内部逻辑自洽
2. 与题材定位保持一致
3. 为剧情发展留下足够空间
4. 避免过于复杂，要服务于故事
"""

    from tools.web_search_tool import web_search
    from tools.knowledge_search_tool import knowledge_search
    
    tools = [web_search, knowledge_search]
    
    return create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=MessagesState,
    )
