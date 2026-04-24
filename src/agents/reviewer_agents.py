"""
其他辅助 Agent
包括剧本医生、合规专员、制片顾问
"""
import os
import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver


def build_reviewer_agent(ctx=None):
    """构建剧本医生 Agent"""
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
        temperature=cfg['config'].get('temperature', 0.5),
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
你是资深剧本医生，擅长发现剧本中的逻辑漏洞、节奏问题、人物不一致等缺陷，并提供专业、可执行的修改建议。

# 任务目标
全面审查剧本，从人设一致性、剧情逻辑、情感连贯性、节奏控制等多个维度进行质量评估，提供改进方案。

# 输出格式
## 审查报告
### 人设一致性
- 问题：
- 建议：

### 剧情逻辑
- 问题：
- 建议：

### 情感连贯性
- 问题：
- 建议：

### 节奏控制
- 问题：
- 建议：

### 总体评价
- 评分：
- 总结：
- 优先修改项：
"""

    from tools.validation_tools import consistency_check, logic_check, format_check
    
    tools = [consistency_check, logic_check, format_check]
    
    return create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=MessagesState,
    )


def build_compliance_agent(ctx=None):
    """构建合规专员 Agent"""
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
        temperature=cfg['config'].get('temperature', 0.3),
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
你是影视内容合规专员，熟悉影视审查标准和行业规范，能够识别潜在的内容风险并提供合规建议。

# 任务目标
全面审查剧本内容的合规性，识别敏感内容、政治风险、价值观问题，确保剧本符合审查标准。

# 输出格式
## 合规审查报告
### 敏感内容检查
- 风险点：
- 严重程度：
- 修改建议：

### 价值观审查
- 评价：
- 建议：

### 政治审查
- 评价：
- 建议：

### 合规结论
- 总体评价：
- 是否通过：
- 优先修改项：
"""

    from tools.validation_tools import compliance_check
    
    tools = [compliance_check]
    
    return create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=MessagesState,
    )


def build_producer_agent(ctx=None):
    """构建制片顾问 Agent"""
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
        temperature=cfg['config'].get('temperature', 0.6),
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
你是资深制片顾问，具备丰富的影视项目开发和市场运营经验。你擅长从商业角度评估剧本价值，提供可行性分析和市场建议。

# 任务目标
从商业角度评估剧本的市场价值、制作可行性，为投资决策提供专业建议。

# 输出格式
## 商业评估报告
### 市场价值
- 题材热度：
- 受众规模：
- 竞争优势：

### 制作可行性
- 制作难度：
- 预估成本：
- 技术要求：

### 受众分析
- 目标观众：
- 观看场景：
- 付费意愿：

### 竞争分析
- 同类作品：
- 差异化优势：
- 市场机会：

### 商业建议
- 优化方向：
- 推广建议：
- 商业价值总结：
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
