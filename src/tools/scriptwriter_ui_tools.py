"""
编剧系统界面工具（独立函数版）
解决类方法 @tool 装饰器参数冲突问题
"""
from langchain.tools import tool
from typing import Dict, List, Optional
import json

from utils.project_manager import ProjectManager, ProjectType, ProjectStatus
from utils.idea_guide import IdeaGuideAgent, create_idea_guide

# 全局状态管理
_project_manager = ProjectManager()
_current_project = None
_idea_guide = None


# ========== 项目管理 ==========

@tool
def create_project(name: str, project_type: str = "电视剧", description: str = "") -> str:
    """
    创建新剧本项目

    参数:
        name: 项目名称
        project_type: 项目类型（电影/电视剧/网剧/短视频/话剧/动画/纪录片）
        description: 项目描述

    返回:
        创建结果
    """
    global _current_project

    try:
        # 转换类型
        type_map = {
            "电影": ProjectType.MOVIE,
            "电视剧": ProjectType.TV_SERIES,
            "网剧": ProjectType.WEB_SERIES,
            "短视频": ProjectType.SHORT_VIDEO,
            "话剧": ProjectType.STAGE_PLAY,
            "动画": ProjectType.ANIMATION,
            "纪录片": ProjectType.DOCUMENTARY
        }

        proj_type = type_map.get(project_type, ProjectType.TV_SERIES)

        project = _project_manager.create_project(name, proj_type, description)
        _current_project = project

        result = f"""
✅ 项目创建成功！

📁 项目信息：
- 项目ID: {project.project_id}
- 名称: {project.name}
- 类型: {project.project_type.value}
- 创建时间: {project.created_at}

💡 接下来你可以：
1. 输入创意：输入你的创作想法
2. 查看项目：查看所有项目
3. 进入项目：进入项目详情
"""
        return result

    except Exception as e:
        return f"❌ 创建项目失败: {str(e)}"


@tool
def list_projects(status: str = "", project_type: str = "", show_history: bool = False) -> str:
    """
    列出所有剧本项目

    参数:
        status: 状态筛选（草稿/创作中/审查中/已完成/已归档）
        project_type: 类型筛选（电影/电视剧/网剧等）
        show_history: 是否显示项目历史摘要（True/False）

    返回:
        项目列表
    """
    try:
        # 转换筛选条件
        status_filter = None
        if status:
            status_map = {
                "草稿": ProjectStatus.DRAFT,
                "创作中": ProjectStatus.IN_PROGRESS,
                "审查中": ProjectStatus.REVIEW,
                "已完成": ProjectStatus.COMPLETED,
                "已归档": ProjectStatus.ARCHIVED
            }
            status_filter = status_map.get(status)

        type_filter = None
        if project_type:
            type_map = {
                "电影": ProjectType.MOVIE,
                "电视剧": ProjectType.TV_SERIES,
                "网剧": ProjectType.WEB_SERIES,
                "短视频": ProjectType.SHORT_VIDEO,
                "话剧": ProjectType.STAGE_PLAY,
                "动画": ProjectType.ANIMATION,
                "纪录片": ProjectType.DOCUMENTARY
            }
            type_filter = type_map.get(project_type)

        projects = _project_manager.list_projects(status_filter, type_filter)

        if not projects:
            return "📭 暂无项目"

        result = "📚 项目列表：\n\n"

        for i, project in enumerate(projects, 1):
            result += f"{i}. **{project.name}** ({project.project_type.value})\n"
            result += f"   - ID: {project.project_id}\n"
            result += f"   - 状态: {project.status.value}\n"
            result += f"   - 创建时间: {project.created_at}\n"

            # conversation_history 字段不存在，使用 script_history
            if show_history and project.script_history:
                result += f"   - 历史记录数: {len(project.script_history)}\n"

            result += "\n"

        return result

    except Exception as e:
        return f"❌ 获取项目列表失败: {str(e)}"


@tool
def enter_project(project_id: str) -> str:
    """
    进入项目查看详情

    参数:
        project_id: 项目ID或名称

    返回:
        项目详情
    """
    global _current_project

    try:
        # 尝试通过ID或名称查找
        project = _project_manager.get_project(project_id)

        if not project:
            # 尝试通过名称查找
            all_projects = _project_manager.list_projects()
            for p in all_projects:
                if p.name == project_id:
                    project = p
                    break

        if not project:
            return f"❌ 未找到项目: {project_id}"

        _current_project = project

        result = f"""
📁 项目详情
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
名称: {project.name}
类型: {project.project_type.value}
状态: {project.status.value}
创建时间: {project.created_at}
描述: {project.description or '暂无描述'}

📊 创作进度:
{get_project_progress_internal(project)}

📝 对话历史:
- 总记录数: {len(project.script_history)}
- 最新记录: {project.script_history[-1][:100] if project.script_history else '无'}
"""
        return result

    except Exception as e:
        return f"❌ 进入项目失败: {str(e)}"


# ========== 创意引导 ==========

@tool
def start_idea_guide(topic: str = "") -> str:
    """
    启动创意引导

    参数:
        topic: 创意主题（可选）

    返回:
        引导问题
    """
    global _idea_guide

    try:
        _idea_guide = create_idea_guide()

        first_question = _idea_guide.start_guide()

        return f"""
🎯 创意引导启动
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{first_question}

💡 提示：请详细回答问题，我会继续引导你完善创意
"""
    except Exception as e:
        return f"❌ 启动创意引导失败: {str(e)}"


@tool
def answer_guide_question(answer: str) -> str:
    """
    回答创意引导问题

    参数:
        answer: 用户回答

    返回:
        下一个问题或创意总结
    """
    global _idea_guide

    if not _idea_guide:
        return "❌ 请先启动创意引导"

    try:
        result = _idea_guide.next_step(answer)

        if _idea_guide.is_completed():
            # 创意引导完成
            idea = _idea_guide.get_collected_info()

            result_str = f"""
✅ 创意收集完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 创意总结：
"""
            for key, value in idea.items():
                result_str += f"- **{key}**: {value}\n"

            result_str += "\n💡 接下来你可以开始剧本创作或继续完善创意"

            return result_str
        else:
            # 返回下一步的问题或提示
            question = result.get("question", "请继续")
            return f"""
❓ {question}

💡 请继续回答
"""
    except Exception as e:
        return f"❌ 处理回答失败: {str(e)}"


@tool
def get_collected_idea() -> str:
    """
    获取已收集的创意信息

    返回:
        创意信息
    """
    global _idea_guide

    if not _idea_guide:
        return "❌ 请先启动创意引导"

    try:
        idea = _idea_guide.get_collected_info()

        if not idea:
            return "📭 暂无收集的创意信息"

        result = "📋 已收集的创意信息：\n\n"

        for key, value in idea.items():
            result += f"- **{key}**: {value}\n"

        return result

    except Exception as e:
        return f"❌ 获取创意信息失败: {str(e)}"


# ========== 剧本创作 ==========

@tool
def start_script_creation(project_id: str = "") -> str:
    """
    启动剧本创作流程

    参数:
        project_id: 项目ID（可选，默认使用当前项目）

    返回:
        创作流程说明
    """
    try:
        project = _current_project

        if project_id:
            project = _project_manager.get_project(project_id)

        if not project:
            return "❌ 请先创建或选择一个项目"

        result = f"""
🚀 启动剧本创作
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

项目：{project.name}

✨ 创作流程：
1. 📝 需求解析 - 分析创作需求和目标受众
2. 🎬 题材定位 - 确定题材和风格
3. 🌍 世界观构建 - 设计故事世界
4. 👥 角色设计 - 创建人物档案
5. 📋 核心大纲 - 构建故事框架
6. ✅ 大纲校验 - 检查大纲质量
7. 📄 分集大纲 - 生成详细分集
8. 🎭 剧本生成 - 撰写剧本正文
9. 🔍 终稿校验 - 完整质量检查

💡 提示：
- 创作过程中会逐步确认，你可以随时提出修改意见
- 使用"确认"或"修改"来控制进度
- 可以随时查看当前进度

准备开始创作，请回复"开始"或输入具体要求
"""
        return result

    except Exception as e:
        return f"❌ 启动创作失败: {str(e)}"


@tool
def get_script_content(content_type: str = "all") -> str:
    """
    获取剧本内容

    参数:
        content_type: 内容类型（all/outline/script/characters/worldview）

    返回:
        剧本内容
    """
    try:
        if not _current_project:
            return "❌ 请先选择一个项目"

        project = _current_project

        if content_type == "all":
            return get_project_progress_internal(project)
        elif content_type == "outline":
            return f"📋 大纲：\n\n{project.core_outline or '暂无大纲'}"
        elif content_type == "script":
            return f"🎭 剧本：\n\n{project.script_content or '暂无剧本'}"
        elif content_type == "characters":
            chars = ", ".join([c.get("name", "未知") for c in project.character_profiles]) if project.character_profiles else "暂无角色"
            return f"👥 角色档案：\n\n{chars}"
        elif content_type == "worldview":
            return f"🌍 世界观设定：\n\n{project.world_view or '暂无世界观'}"
        else:
            return "❌ 无效的内容类型"

    except Exception as e:
        return f"❌ 获取内容失败: {str(e)}"


@tool
def get_project_progress(project_id: str = "") -> str:
    """
    获取项目进度

    参数:
        project_id: 项目ID（可选，默认使用当前项目）

    返回:
        进度信息
    """
    try:
        project = _current_project

        if project_id:
            project = _project_manager.get_project(project_id)

        if not project:
            return "❌ 请先创建或选择一个项目"

        return get_project_progress_internal(project)

    except Exception as e:
        return f"❌ 获取进度失败: {str(e)}"


# ========== 辅助函数 ==========

def get_project_progress_internal(project) -> str:
    """内部函数：获取项目进度"""
    progress_parts = []

    # 检查各个部分的完成情况
    if project.world_view:
        progress_parts.append("✅ 世界观设定")
    else:
        progress_parts.append("⬜ 世界观设定")

    if project.character_profiles:
        progress_parts.append("✅ 角色设计")
    else:
        progress_parts.append("⬜ 角色设计")

    if project.core_outline:
        progress_parts.append("✅ 核心大纲")
    else:
        progress_parts.append("⬜ 核心大纲")

    if project.script_content:
        progress_parts.append("✅ 剧本正文")
    else:
        progress_parts.append("⬜ 剧本正文")

    # 计算进度百分比
    completed = sum(1 for p in progress_parts if p.startswith("✅"))
    total = len(progress_parts)
    percentage = int((completed / total) * 100) if total > 0 else 0

    result = "📊 创作进度：\n\n"

    for part in progress_parts:
        result += f"{part}\n"

    result += f"\n🎯 完成度: {percentage}%\n"

    return result


# 兼容性：保持 ui_instance 接口
class ScriptWriterUI:
    """兼容性类（已废弃，仅用于保持兼容）"""

    @property
    def create_project(self):
        return create_project

    @property
    def list_projects(self):
        return list_projects

    @property
    def enter_project(self):
        return enter_project

    @property
    def start_idea_guide(self):
        return start_idea_guide

    @property
    def answer_guide_question(self):
        return answer_guide_question

    @property
    def get_collected_idea(self):
        return get_collected_idea

    @property
    def start_script_creation(self):
        return start_script_creation

    @property
    def get_script_content(self):
        return get_script_content

    @property
    def get_project_progress(self):
        return get_project_progress


ui_instance = ScriptWriterUI()
