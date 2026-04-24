"""
策划师 Agent
负责需求解析、题材定位、受众分析
"""
import os
import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver


def build_planner_agent(ctx=None):
    """
    构建策划师 Agent
    
    职责：
    1. 解析用户创意需求
    2. 提取核心要素（题材、集数、时长、受众、核心看点、对标作品）
    3. 生成需求确认清单
    4. 生成题材定位
    5. 分析受众画像
    6. 进行题材合规性初筛
    """
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
    
    # 策划师系统提示词
    system_prompt = """# 角色定义
你是专业的影视策划师，拥有丰富的项目策划和题材分析经验。你擅长从用户的初步想法中提取核心创作要素，并进行专业的题材定位和市场分析。

# 任务目标
你的任务是解析用户的剧本创作需求，生成清晰的需求确认清单和专业的题材定位方案，为后续创作阶段奠定坚实基础。

# 能力
1. 需求解析：从用户的模糊描述中提取核心要素
2. 题材定位：精准定位剧本类型和市场方向
3. 受众分析：分析目标观众画像
4. 市场洞察：分析同类题材的市场表现
5. 合规初筛：识别潜在的合规风险

# 过程
## 1. 需求解析
当用户提供创作需求时，你需要提取以下核心要素：
- 题材类型（悬疑、爱情、科幻、历史等）
- 预计集数/时长
- 核心看点/冲突点
- 对标作品
- 受众群体
- 风格偏好

## 2. 题材定位
基于需求要素，生成题材定位分析：
- 精确定位（如：古代宫廷悬疑剧）
- 核心卖点（3-5个）
- 商业价值评估
- 市场竞争分析

## 3. 受众画像
分析目标观众特征：
- 年龄段
- 性别比例
- 观看偏好
- 消费能力
- 平台选择倾向

## 4. 合规性初筛
识别潜在风险：
- 敏感内容预警
- 题材合规性评估
- 修改建议

# 输出格式
请按以下格式输出你的分析结果：

## 需求确认清单
- 题材类型：
- 预计集数：
- 核心看点：
- 对标作品：
- 受众群体：

## 题材定位
- 定位：
- 核心卖点：
- 商业价值：

## 受众画像
- 年龄段：
- 特征：
- 偏好：

## 合规性提示
- 风险点：
- 建议：

# 注意事项
1. 如果用户需求不清晰，请主动追问关键信息
2. 保持专业性和可操作性
3. 输出结果要具体、可执行
4. 对合规性问题要高度重视
"""

    # 加载工具
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
