"""
多智能体编剧系统 - Agent 定义
包含 7 个专业编剧智能体
"""

from agents.planner_agent import build_planner_agent
from agents.worldview_agent import build_worldview_agent
from agents.character_agent import build_character_agent
from agents.writer_agent import build_writer_agent
from agents.reviewer_agents import (
    build_reviewer_agent,
    build_compliance_agent,
    build_producer_agent
)

# 为兼容性创建别名
build_genre_agent = build_producer_agent  # 题材定位功能由策划师和制片顾问共同完成

__all__ = [
    "build_planner_agent",
    "build_genre_agent",  # 别名
    "build_worldview_agent",
    "build_character_agent",
    "build_writer_agent",
    "build_reviewer_agent",
    "build_compliance_agent",
    "build_producer_agent"
]
