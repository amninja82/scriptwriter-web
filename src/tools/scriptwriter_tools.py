"""
编剧工具模块
包含知识库搜索、在线搜索、校验等工具
"""

from tools.knowledge_search_tool import knowledge_search
from tools.web_search_tool import web_search
from tools.validation_tools import (
    consistency_check,
    logic_check,
    compliance_check,
    format_check
)
from tools.foreshadowing_tool import add_foreshadowing, check_foreshadowing

__all__ = [
    "knowledge_search",
    "web_search",
    "consistency_check",
    "logic_check",
    "compliance_check",
    "format_check",
    "add_foreshadowing",
    "check_foreshadowing"
]
