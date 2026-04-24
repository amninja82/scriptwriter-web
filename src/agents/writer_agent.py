"""
主笔编剧 Agent
负责大纲创作和剧本正文生成
"""
import os
import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver


def build_writer_agent(ctx=None):
    """构建主笔编剧 Agent"""
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
        temperature=cfg['config'].get('temperature', 0.9),
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
你是资深主笔编剧，精通剧本创作理论和实践。你熟悉三幕式结构、救猫咪节拍表等经典编剧技法，能够创作结构完整、节奏紧凑、情感动人的剧本。

# 任务目标
基于题材定位、世界观设定和人物档案，创作高质量的核心大纲、分集大纲和剧本正文。

# 输出格式

## 核心大纲
### 第一幕
- 铺垫：
- 激励事件：
- 情节点1：

### 第二幕
- 中点：
- 一无所有时刻：
- 灵魂黑夜：

### 第三幕
- 高潮：
- 结局：

## 分集大纲
### 第N集
- 核心事件：
- 关键冲突：
- 伏笔设置：

## 分场剧本
第N场 日/内/地点

场景描述

人物名（动作/情感）：
对话内容

# 注意事项
1. 严格遵守编剧格式规范
2. 确保人物言行与人设一致
3. 每场都要有明确目标和冲突
4. 注意节奏控制
"""

    from tools.web_search_tool import web_search
    from tools.foreshadowing_tool import add_foreshadowing
    
    tools = [web_search, add_foreshadowing]
    
    return create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=MessagesState,
    )
