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
from tools.file_upload_tool import (
    upload_text_file_to_knowledge,
    upload_url_to_knowledge,
    batch_upload_files_to_knowledge,
    list_knowledge_datasets,
    delete_knowledge_document
)
from tools.project_history_tool import (
    save_conversation_to_project,
    load_project_history,
    search_all_projects,
    search_project,
    switch_to_project,
    get_project_summary
)
from tools.smart_search_tool import (
    smart_search_and_classify,
    search_multiple_sources,
    search_and_compare
)

__all__ = [
    "knowledge_search",
    "web_search",
    "consistency_check",
    "logic_check",
    "compliance_check",
    "format_check",
    "add_foreshadowing",
    "check_foreshadowing",
    "upload_text_file_to_knowledge",
    "upload_url_to_knowledge",
    "batch_upload_files_to_knowledge",
    "list_knowledge_datasets",
    "delete_knowledge_document",
    "save_conversation_to_project",
    "load_project_history",
    "search_all_projects",
    "search_project",
    "switch_to_project",
    "get_project_summary",
    "smart_search_and_classify",
    "search_multiple_sources",
    "search_and_compare"
]
