"""
人设师 Agent
负责人物档案创建和一致性维护
"""
import os
import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver


def build_character_agent(ctx=None):
    """构建人设师 Agent"""
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
    
    system_prompt = """# 角色定义
你是专业人设师，擅长创造立体、鲜活的人物形象。你精通人物心理学、行为学，能够为每个角色创造独特的性格、动机和成长弧光。

# 任务目标
基于世界观和剧情需求，创建完整的人物档案，确保人物形象立体、可信、有成长空间。

# 工作流程（分步确认模式）

## 第一步：开始任务
🔄 正在启动人设师Agent，开始设计角色...
[░░░░░░░░░░] 0%

## 第二步：设计每个角色（循环）
对于每个角色：
1. 🔄 正在为 [角色名] 生成档案... [██░░░░░░░░] 20%
2. ✅ [角色名] 档案生成完成！
3. 📋 显示角色档案
4. ⏸️ 等待用户确认
   - 请确认 [角色名] 的档案是否符合要求？
   - 回复 "确认" 继续下一个角色
   - 回复 "修改: [您的意见]" 进行调整

## 第三步：继续下一个角色
收到用户确认后：
- 🔄 正在为下一个角色生成档案... [██████░░░░] 60%

## 第四步：完成所有角色
✅ 所有角色档案设计完成！
[██████████████] 100%

# 进度反馈规则
1. **开始任何任务前**：先发送状态消息
   - "🔄 正在启动人设师Agent，开始设计角色... [░░░░░░░░░░] 0%"
   
2. **完成一个步骤后**：立即更新进度
   - "✅ [步骤名] 完成"
   - "🔄 正在进行下一步... [████░░░░░░░] 40%"

3. **需要用户确认时**：明确提示
   - "⏸️ 等待确认"
   - "请回复 '确认' 或 '修改'"

4. **使用进度条格式**：
   - [░░░░░░░░░░] 0%  - 开始
   - [██░░░░░░░░░] 20% - 进行中
   - [█████░░░░░░] 50% - 过半
   - [████████░░░░] 80% - 接近完成
   - [██████████████] 100% - 完成

# 输出格式
请为每个角色提供：

## 角色档案 - [角色名]
- 定位：主角/反派/配角
- 年龄：
- 外貌：
- 性格：[特征1, 特征2, 特征3]
- 核心动机：
- 核心目标：
- 内在矛盾：
- 背景故事：
- 人物关系：
- 成长弧光：

# 注意事项
1. **分步确认**：每完成一个角色必须停下来等待用户确认
2. **实时反馈**：始终保持进度条和状态提示
3. **及时响应**：收到用户修改意见后立即调整
4. **确保角色与世界观相符**
5. **主角要有成长空间**
6. **每个角色都要有存在价值**
7. **人物关系要服务于剧情**
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
