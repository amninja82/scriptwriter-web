"""
多智能体编剧系统 - LangGraph 状态机
定义 9 个核心节点的编剧工作流
"""
from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage

from .scriptwriter_state import ScriptWriterState
from agents.scriptwriter_agents import (
    build_planner_agent,
    build_worldview_agent,
    build_character_agent,
    build_writer_agent,
    build_reviewer_agent,
    build_compliance_agent,
    build_producer_agent
)


def create_scriptwriter_graph():
    """
    创建多智能体编剧状态机
    
    工作流节点：
    1. requirement_analysis - 需求解析
    2. genre_positioning - 题材定位
    3. worldview_creation - 世界观与人设
    4. core_outline - 核心大纲
    5. outline_validation - 大纲校验
    6. episode_outline - 分集/分场大纲
    7. script_generation - 剧本正文生成
    8. final_validation - 终稿校验
    9. modification - 修改迭代
    """
    
    # 初始化所有 Agent
    planner_agent = build_planner_agent()
    worldview_agent = build_worldview_agent()
    character_agent = build_character_agent()
    writer_agent = build_writer_agent()
    reviewer_agent = build_reviewer_agent()
    compliance_agent = build_compliance_agent()
    producer_agent = build_producer_agent()
    
    # 创建状态机图
    workflow = StateGraph(ScriptWriterState)
    
    # ========== 节点定义 ==========
    
    def requirement_analysis_node(state: dict):
        """节点1: 需求解析"""
        print("\n📋 [节点1] 需求解析...")
        
        messages = [
            HumanMessage(content=f"""
请解析以下剧本创作需求：

{state.get('user_requirement', '')}

请提取核心要素：
- 题材类型
- 预计集数/时长
- 核心看点
- 对标作品
- 受众群体
- 风格偏好

并进行题材定位和受众分析。
""")
        ]
        
        result = planner_agent.invoke({"messages": messages})
        
        new_state = state.copy()
        new_state["parsed_requirement"] = result["messages"][-1].content if result["messages"] else ""
        new_state["current_stage"] = "需求解析完成"
        new_state["messages"] = add_messages(state.get("messages", []), result["messages"])
        
        return new_state
    
    def genre_positioning_node(state: dict):
        """节点2: 题材定位"""
        print("\n🎯 [节点2] 题材定位...")
        
        messages = [
            HumanMessage(content=f"""
基于需求解析结果，进行深入的题材定位和市场分析：

{state.get('parsed_requirement', '')}

请提供：
1. 精确的题材定位
2. 核心卖点（3-5个）
3. 商业价值评估
4. 受众画像
5. 市场竞争分析
6. 合规性初筛
""")
        ]
        
        result = producer_agent.invoke({"messages": messages})
        
        new_state = state.copy()
        new_state["genre_positioning"] = result["messages"][-1].content if result["messages"] else ""
        new_state["audience_profile"] = result["messages"][-1].content if result["messages"] else ""
        new_state["current_stage"] = "题材定位完成"
        new_state["messages"] = add_messages(state.get("messages", []), result["messages"])
        
        return new_state
    
    def worldview_creation_node(state: dict):
        """节点3: 世界观与人设"""
        print("\n🌍 [节点3] 世界观与人设构建...")
        
        new_state = state.copy()
        
        # 先构建世界观
        worldview_messages = [
            HumanMessage(content=f"""
基于题材定位，构建完整的世界观设定：

{state.get('genre_positioning', '')}

请创建详细的世界观设定，包括：
1. 时间背景与历史
2. 社会结构
3. 文化体系
4. 地理环境
5. 特殊规则（如适用）
""")
        ]
        
        worldview_result = worldview_agent.invoke({"messages": worldview_messages})
        new_state["world_view"] = worldview_result["messages"][-1].content if worldview_result["messages"] else ""
        
        # 再创建人设
        character_messages = [
            HumanMessage(content=f"""
基于世界观设定，创建核心人物档案：

世界观：
{new_state.get('world_view', '')}

请为所有核心角色创建详细档案，包括：
1. 角色定位
2. 性格特征
3. 核心动机
4. 背景故事
5. 人物关系
6. 成长弧光
""")
        ]
        
        character_result = character_agent.invoke({"messages": character_messages})
        new_state["character_profiles"] = [character_result["messages"][-1].content if character_result["messages"] else ""]
        
        new_state["current_stage"] = "世界观与人设完成"
        current_msgs = state.get("messages", [])
        new_state["messages"] = add_messages(
            current_msgs,
            worldview_result["messages"] + character_result["messages"]
        )
        
        return new_state
    
    def core_outline_node(state: dict):
        """节点4: 核心大纲"""
        print("\n📝 [节点4] 核心大纲创作...")
        
        messages = [
            HumanMessage(content=f"""
基于以下信息创作核心大纲：

题材定位：
{state.get('genre_positioning', '')}

世界观：
{state.get('world_view', '')}

人物档案：
{state.get('character_profiles', [''])[0] if state.get('character_profiles') else ''}

请采用三幕式结构创作核心大纲，包括：
1. 第一幕：铺垫、激励事件、情节点1
2. 第二幕：中点、一无所有时刻、灵魂黑夜
3. 第三幕：高潮、结局

标注关键冲突、反转、伏笔、人物弧光节点。
""")
        ]
        
        result = writer_agent.invoke({"messages": messages})
        
        new_state = state.copy()
        new_state["core_outline"] = result["messages"][-1].content if result["messages"] else ""
        new_state["current_stage"] = "核心大纲完成"
        new_state["messages"] = add_messages(state.get("messages", []), result["messages"])
        
        return new_state
    
    def outline_validation_node(state: dict):
        """节点5: 大纲校验"""
        print("\n✅ [节点5] 大纲校验...")
        
        messages = [
            HumanMessage(content=f"""
请审查以下核心大纲：

{state.get('core_outline', '')}

人物档案：
{state.get('character_profiles', [''])[0] if state.get('character_profiles') else ''}

请从以下维度校验：
1. 人设一致性
2. 剧情逻辑
3. 合规性
4. 格式规范

如果发现问题，请给出修改建议。
""")
        ]
        
        result = reviewer_agent.invoke({"messages": messages})
        
        # 合规审查
        genre_text = state.get('genre_positioning', '')
        genre_info = genre_text[:200] if isinstance(genre_text, str) else ''
        
        compliance_messages = [
            HumanMessage(content=f"""
请进行合规性审查：

核心大纲：
{state.get('core_outline', '')}

题材：{genre_info}
""")
        ]
        
        compliance_result = compliance_agent.invoke({"messages": compliance_messages})
        
        new_state = state.copy()
        new_state["validation_reports"] = [
            {"type": "大纲审查", "content": result["messages"][-1].content if result["messages"] else ""},
            {"type": "合规审查", "content": compliance_result["messages"][-1].content if compliance_result["messages"] else ""}
        ]
        new_state["is_valid"] = True
        new_state["current_stage"] = "大纲校验完成"
        
        current_msgs = state.get("messages", [])
        new_state["messages"] = add_messages(
            current_msgs,
            result["messages"] + compliance_result["messages"]
        )
        
        return new_state
    
    def episode_outline_node(state: dict):
        """节点6: 分集/分场大纲"""
        print("\n📚 [节点6] 分集/分场大纲...")
        
        messages = [
            HumanMessage(content=f"""
将核心大纲拆解为详细的分集/分场大纲：

核心大纲：
{state.get('core_outline', '')}

请创建：
1. 分集概述（每集核心事件）
2. 分场大纲（每场场景的目标、冲突、节奏）
3. 伏笔设置计划
""")
        ]
        
        result = writer_agent.invoke({"messages": messages})
        
        new_state = state.copy()
        new_state["episode_outlines"] = [result["messages"][-1].content if result["messages"] else ""]
        new_state["current_stage"] = "分集/分场大纲完成"
        new_state["messages"] = add_messages(state.get("messages", []), result["messages"])
        
        return new_state
    
    def script_generation_node(state: dict):
        """节点7: 剧本正文生成"""
        print("\n✍️ [节点7] 剧本正文生成...")
        
        messages = [
            HumanMessage(content=f"""
基于分场大纲，生成剧本正文：

分场大纲：
{state.get('episode_outlines', [''])[0] if state.get('episode_outlines') else ''}

人物档案：
{state.get('character_profiles', [''])[0] if state.get('character_profiles') else ''}

请按标准剧本格式生成正文，包括：
1. 场景标头（场号、时间、地点）
2. 场景描述
3. 人物对话
4. 动作描写
5. 情感提示

确保人物言行与人设一致，每场都有明确目标和冲突。
""")
        ]
        
        result = writer_agent.invoke({"messages": messages})
        
        new_state = state.copy()
        new_state["script_content"] = result["messages"][-1].content if result["messages"] else ""
        new_state["current_version"] = 1
        new_state["script_history"] = [{"version": 1, "content": result["messages"][-1].content if result["messages"] else ""}]
        new_state["current_stage"] = "剧本初稿完成"
        new_state["messages"] = add_messages(state.get("messages", []), result["messages"])
        
        return new_state
    
    def final_validation_node(state: dict):
        """节点8: 终稿校验"""
        print("\n🔍 [节点8] 终稿校验...")
        
        new_state = state.copy()
        
        # 综合校验
        messages = [
            HumanMessage(content=f"""
请对剧本进行终稿全面校验：

剧本内容：
{state.get('script_content', '')}

人物档案：
{state.get('character_profiles', [''])[0] if state.get('character_profiles') else ''}

核心大纲：
{state.get('core_outline', '')}

请检查：
1. 人设一致性
2. 剧情逻辑
3. 伏笔回收
4. 合规性
5. 格式标准化
""")
        ]
        
        result = reviewer_agent.invoke({"messages": messages})
        
        # 合规审查
        compliance_messages = [
            HumanMessage(content=f"""
终稿合规性审查：

剧本内容：
{state.get('script_content', '')[:5000]}...
""")
        ]
        
        compliance_result = compliance_agent.invoke({"messages": compliance_messages})
        
        new_state["validation_reports"] = state.get("validation_reports", []) + [
            {"type": "终稿审查", "content": result["messages"][-1].content if result["messages"] else ""},
            {"type": "终稿合规审查", "content": compliance_result["messages"][-1].content if compliance_result["messages"] else ""}
        ]
        new_state["current_stage"] = "终稿校验完成"
        
        current_msgs = state.get("messages", [])
        new_state["messages"] = add_messages(
            current_msgs,
            result["messages"] + compliance_result["messages"]
        )
        
        return new_state
    
    def modification_node(state: dict):
        """节点9: 修改迭代"""
        print("\n🔄 [节点9] 修改迭代...")
        
        if not state.get("modification_requests"):
            print("无修改请求，跳过修改阶段")
            return state
        
        messages = [
            HumanMessage(content=f"""
根据以下修改意见修改剧本：

修改意见：
{chr(10).join(state.get('modification_requests', []))}

当前剧本：
{state.get('script_content', '')}

请进行针对性修改，修改后保持整体连贯性。
""")
        ]
        
        result = writer_agent.invoke({"messages": messages})
        
        new_state = state.copy()
        new_version = state.get("current_version", 1) + 1
        new_state["script_content"] = result["messages"][-1].content if result["messages"] else ""
        new_state["current_version"] = new_version
        new_state["script_history"] = state.get("script_history", []) + [{
            "version": new_version,
            "content": result["messages"][-1].content if result["messages"] else ""
        }]
        new_state["current_stage"] = f"剧本第 {new_version} 版完成"
        new_state["messages"] = add_messages(state.get("messages", []), result["messages"])
        
        return new_state
    
    # ========== 添加节点 ==========
    workflow.add_node("requirement_analysis", requirement_analysis_node)
    workflow.add_node("genre_positioning", genre_positioning_node)
    workflow.add_node("worldview_creation", worldview_creation_node)
    workflow.add_node("core_outline", core_outline_node)
    workflow.add_node("outline_validation", outline_validation_node)
    workflow.add_node("episode_outline", episode_outline_node)
    workflow.add_node("script_generation", script_generation_node)
    workflow.add_node("final_validation", final_validation_node)
    workflow.add_node("modification", modification_node)
    
    # ========== 设置入口 ==========
    workflow.set_entry_point("requirement_analysis")
    
    # ========== 添加边 ==========
    workflow.add_edge("requirement_analysis", "genre_positioning")
    workflow.add_edge("genre_positioning", "worldview_creation")
    workflow.add_edge("worldview_creation", "core_outline")
    workflow.add_edge("core_outline", "outline_validation")
    workflow.add_edge("outline_validation", "episode_outline")
    workflow.add_edge("episode_outline", "script_generation")
    workflow.add_edge("script_generation", "final_validation")
    workflow.add_edge("final_validation", "modification")
    workflow.add_edge("modification", END)
    
    return workflow.compile()
