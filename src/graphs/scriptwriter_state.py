"""
多智能体编剧系统状态定义
定义 LangGraph 状态机使用的状态结构
"""
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


# 定义消息类型
MessagesType = List[BaseMessage]


class ScriptWriterState(TypedDict):
    """编剧工作流状态"""
    
    # 消息历史 - 使用 Annotated 包装
    messages: Annotated[MessagesType, add_messages]
    
    # 需求解析阶段
    user_requirement: str  # 用户原始需求
    parsed_requirement: str  # 解析后的需求（字符串形式）
    
    # 题材定位阶段
    genre_positioning: str  # 题材定位（字符串形式）
    audience_profile: str  # 受众画像（字符串形式）
    
    # 世界观与人设阶段
    world_view: str  # 世界观设定
    character_profiles: List[str]  # 人物档案（列表形式）
    
    # 大纲阶段
    core_outline: str  # 核心大纲
    episode_outlines: List[str]  # 分集/分场大纲（列表形式）
    
    # 剧本生成阶段
    script_content: str  # 剧本正文
    
    # 校验阶段
    validation_reports: List[Dict[str, Any]]  # 校验报告
    
    # 伏笔管理
    foreshadowings: List[Dict[str, Any]]  # 伏笔列表
    
    # 版本管理
    current_version: int  # 当前版本号
    script_history: List[Dict[str, Any]]  # 剧本历史
    
    # 修改阶段
    modification_requests: List[str]  # 修改意见列表
    
    # 工作流状态
    current_stage: str  # 当前所处阶段
    is_valid: bool  # 当前阶段是否通过校验
    
    # 元数据
    metadata: Dict[str, Any]  # 其他元数据
    
    # 检查点信息（用于恢复）
    checkpoint_data: Optional[Dict[str, Any]]  # 检查点数据
