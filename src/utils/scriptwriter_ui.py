"""
编剧系统用户界面
整合项目管理、创意引导、剧本创作功能
"""
from langchain.tools import tool
from typing import Dict, List, Optional
import json

from utils.project_manager import ProjectManager, ProjectType, ProjectStatus
from utils.idea_guide import IdeaGuideAgent, create_idea_guide


class ScriptWriterUI:
    """编剧系统用户界面"""
    
    def __init__(self):
        self.project_manager = ProjectManager()
        self.current_project = None
        self.idea_guide = None
    
    # ========== 项目管理 ==========
    
    @tool
    def create_project(self, name: str, project_type: str, description: str = "") -> str:
        """
        创建新剧本项目
        
        参数:
            name: 项目名称
            project_type: 项目类型（电影/电视剧/网剧/短视频/话剧/动画/纪录片）
            description: 项目描述
        
        返回:
            创建结果
        """
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
            
            project = self.project_manager.create_project(name, proj_type, description)
            
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
    def list_projects(self, status: str = "", project_type: str = "", show_history: bool = False) -> str:
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
                    "网剧": ProjectType.WEB_SERIES
                }
                type_filter = type_map.get(project_type)

            projects = self.project_manager.list_projects(status_filter, type_filter)

            if not projects:
                return "📭 暂无项目，你可以创建一个新项目！"

            result = "📚 剧本项目列表\n\n"
            for i, proj in enumerate(projects, 1):
                result += f"""
{i}. {proj.name} ({proj.project_type.value})
   ID: {proj.project_id}
   状态: {proj.status.value}
   描述: {proj.description or '暂无描述'}
   创建时间: {proj.created_at}
   最后修改: {proj.updated_at}
"""

            result += f"\n总计: {len(projects)} 个项目"

            # 如果需要显示历史摘要，使用项目历史工具
            if show_history and projects:
                result += "\n\n" + "="*60
                result += "\n📜 项目历史摘要\n\n"

                from tools.project_history_tool import get_project_summary
                for proj in projects[:3]:  # 最多显示前3个项目的历史
                    try:
                        summary = get_project_summary(proj.project_id)
                        result += f"【{proj.name}】\n{summary}\n\n"
                    except Exception as e:
                        result += f"【{proj.name}】历史获取失败: {str(e)}\n\n"

                if len(projects) > 3:
                    result += f"...还有 {len(projects) - 3} 个项目未显示历史\n"

            return result

        except Exception as e:
            return f"❌ 获取项目列表失败: {str(e)}"
    
    @tool
    def enter_project(self, project_id: str, load_history: bool = True) -> str:
        """
        进入项目详情

        参数:
            project_id: 项目 ID
            load_history: 是否加载项目历史对话（默认 True）

        返回:
            项目详情和下一步操作提示
        """
        try:
            project = self.project_manager.get_project(project_id)

            if not project:
                return f"❌ 项目不存在: {project_id}"

            self.current_project = project

            result = f"""
✅ 已进入项目：{project.name}

📋 项目信息：
- ID: {project.project_id}
- 类型: {project.project_type.value}
- 状态: {project.status.value}
- 当前版本: v{project.current_version}

💼 项目内容：
"""

            if project.idea_requirement:
                result += f"- 创意需求: {project.idea_requirement[:50]}...\n"
            else:
                result += "- 创意需求: 未填写\n"

            if project.core_outline:
                result += f"- 核心大纲: 已生成\n"
            else:
                result += "- 核心大纲: 未生成\n"

            if project.script_content:
                result += f"- 剧本正文: 已生成（v{project.current_version}）\n"
            else:
                result += "- 剧本正文: 未生成\n"

            result += f"""
🎯 可用操作：
1. 输入创意：开始需求采集
2. 开始创作：启动剧本创作流程
3. 查看进度：查看创作进度
4. 返回列表：返回项目列表
5. 切换项目：切换到其他项目
"""

            # 如果需要加载历史对话
            if load_history:
                try:
                    from tools.project_history_tool import _load_project_history_impl
                    history = _load_project_history_impl(project_id, limit=10)
                    if "未找到" not in history:
                        result += f"\n---\n\n{history}"
                except Exception as e:
                    result += f"\n⚠️ 加载历史对话失败: {str(e)}"

            return result

        except Exception as e:
            return f"❌ 进入项目失败: {str(e)}"
    
    # ========== 创意引导 ==========
    
    @tool
    def start_idea_guide(self) -> str:
        """
        开始创意引导（对话式需求采集）
        
        返回:
            第一个问题
        """
        if not self.current_project:
            return "❌ 请先进入一个项目！"
        
        self.idea_guide = create_idea_guide()
        first_question = self.idea_guide.start_guide()
        
        return f"""
🎬 创意引导已启动

{first_question}

💡 提示：你可以随时回答，系统会逐步引导你完善需求。
"""
    
    @tool
    def answer_guide_question(self, answer: str) -> str:
        """
        回答创意引导问题
        
        参数:
            answer: 你的回答
        
        返回:
            下一个问题或完成信息
        """
        if not self.idea_guide:
            return "❌ 创意引导未启动，请先运行 start_idea_guide"
        
        result = self.idea_guide.next_step(answer)
        
        if result["status"] == "continue":
            return f"""
{result['next_question']}

📝 已收集信息：
{len(result['collected_info'])}/{len(self.idea_guide.guide.steps)}
"""
        elif result["status"] == "completed":
            # 保存到项目
            if self.current_project:
                self.current_project.save_content("idea_requirement", result.get("requirement_report", ""))
                self.current_project.save_content("requirement_details", result.get("collected_info", {}))
                self.current_project.update_status(ProjectStatus.IN_PROGRESS)
                self.project_manager.save_projects()
            
            return f"""
✅ 创意引导完成！

📋 需求采集摘要：
{result.get('requirement_report', '')}

🎯 下一步：
1. 查看需求：确认需求细节
2. 开始创作：启动剧本创作流程
3. 修改需求：重新采集创意
"""
        
        return "❌ 未知状态"
    
    @tool
    def get_collected_idea(self) -> str:
        """
        查看已采集的创意信息
        
        返回:
            已收集的信息摘要
        """
        if not self.idea_guide:
            return "❌ 创意引导未启动"
        
        if not self.idea_guide.is_completed():
            return "📝 创意采集中... 请先完成引导"
        
        return self.idea_guide.get_summary()
    
    # ========== 剧本创作 ==========
    
    @tool
    def start_script_creation(self) -> str:
        """
        开始剧本创作（使用完整的多智能体系统）
        
        返回:
            创作开始信息
        """
        if not self.current_project:
            return "❌ 请先进入一个项目！"
        
        if not self.current_project.idea_requirement:
            return "❌ 请先完成创意引导（输入创意）！"
        
        try:
            from agents.scriptwriter_system import create_scriptwriter_system
            
            system = create_scriptwriter_system()
            result = system.create_script(self.current_project.idea_requirement)
            
            # 保存结果
            if result.get("success"):
                self.current_project.save_content("genre_positioning", result.get("genre_positioning", ""))
                self.current_project.save_content("world_view", result.get("world_view", ""))
                self.current_project.save_content("character_profiles", result.get("character_profiles", []))
                self.current_project.save_content("core_outline", result.get("core_outline", ""))
                self.current_project.save_content("episode_outlines", result.get("episode_outlines", []))
                self.current_project.save_content("script_content", result.get("script_content", ""))
                self.current_project.save_content("validation_reports", result.get("validation_reports", []))
                self.current_project.update_status(ProjectStatus.COMPLETED)
                self.project_manager.save_projects()
                
                return f"""
✅ 剧本创作完成！

📊 创作结果：
- 当前阶段: {result.get('current_stage')}
- 当前版本: v{result.get('current_version')}
- 题材定位: 已完成
- 世界观: 已完成
- 人物档案: {len(result.get('character_profiles', []))} 个角色
- 分集大纲: 已完成
- 剧本正文: 已生成
- 校验报告: {len(result.get('validation_reports', []))} 份

💡 下一步：
1. 查看剧本：查看完整剧本内容
2. 修改剧本：提出修改意见
3. 导出剧本：导出剧本文件
"""
            else:
                return f"❌ 创作失败: {result.get('error')}"
                
        except Exception as e:
            return f"❌ 创作出错: {str(e)}"
    
    @tool
    def get_script_content(self) -> str:
        """
        获取剧本内容
        
        返回:
            剧本正文
        """
        if not self.current_project:
            return "❌ 请先进入一个项目！"
        
        if not self.current_project.script_content:
            return "❌ 剧本尚未生成，请先开始创作！"
        
        return f"""
📄 剧本正文（v{self.current_project.current_version}）

{self.current_project.script_content[:2000]}...
{'...' if len(self.current_project.script_content) > 2000 else ''}

💡 提示：剧本较长，只显示前2000字符。完整剧本可通过导出功能获取。
"""
    
    @tool
    def get_project_progress(self) -> str:
        """
        查看项目进度
        
        返回:
            项目进度报告
        """
        if not self.current_project:
            return "❌ 请先进入一个项目！"
        
        progress = []
        
        # 检查各阶段完成情况
        stages = {
            "创意需求": bool(self.current_project.idea_requirement),
            "题材定位": bool(self.current_project.requirement_details.get("genre")),
            "世界观": bool(self.current_project.world_view),
            "人物档案": bool(self.current_project.character_profiles),
            "核心大纲": bool(self.current_project.core_outline),
            "分集大纲": bool(self.current_project.episode_outlines),
            "剧本正文": bool(self.current_project.script_content),
        }
        
        completed = sum(stages.values())
        total = len(stages)
        
        progress.append(f"📊 创作进度：{completed}/{total} ({int(completed/total*100)}%)\n")
        
        for stage, done in stages.items():
            icon = "✅" if done else "⬜"
            progress.append(f"{icon} {stage}")
        
        progress.append(f"\n📌 项目状态: {self.current_project.status.value}")
        progress.append(f"📌 当前版本: v{self.current_project.current_version}")
        
        return "\n".join(progress)


# 创建全局实例
ui_instance = ScriptWriterUI()
