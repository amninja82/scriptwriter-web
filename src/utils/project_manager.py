"""
项目管理模块
提供剧本项目的创建、管理功能
"""
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class ProjectType(str, Enum):
    """剧本项目类型"""
    MOVIE = "电影"
    TV_SERIES = "电视剧"
    WEB_SERIES = "网剧"
    SHORT_VIDEO = "短视频"
    STAGE_PLAY = "话剧"
    ANIMATION = "动画"
    DOCUMENTARY = "纪录片"


class ProjectStatus(str, Enum):
    """项目状态"""
    DRAFT = "草稿"
    IN_PROGRESS = "创作中"
    REVIEW = "审查中"
    COMPLETED = "已完成"
    ARCHIVED = "已归档"


class ScriptProject:
    """剧本项目类"""
    
    def __init__(
        self,
        name: str,
        project_type: ProjectType,
        description: str = "",
        creator: str = "user"
    ):
        self.project_id = str(uuid.uuid4())
        self.name = name
        self.project_type = project_type
        self.description = description
        self.status = ProjectStatus.DRAFT
        self.creator = creator
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        
        # 项目内容
        self.idea_requirement = ""
        self.requirement_details = {}
        self.genre_positioning = {}
        self.world_view = ""
        self.character_profiles = []
        self.core_outline = ""
        self.episode_outlines = []
        self.script_content = ""
        self.validation_reports = []
        self.current_version = 0
        self.script_history = []
        
        # 创意引导状态
        self.引导状态 = {
            "current_step": "idea",
            "completed_steps": [],
            "pending_steps": [
                "idea",           # 创意输入
                "genre",          # 题材类型
                "audience",       # 受众群体
                "episodes",       # 集数/时长
                "style",          # 风格偏好
                "reference"       # 对标作品
            ]
        }
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "project_type": self.project_type.value,
            "description": self.description,
            "status": self.status.value,
            "creator": self.creator,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "引导状态": self.引导状态,
            "content": {
                "idea_requirement": self.idea_requirement,
                "requirement_details": self.requirement_details,
                "current_version": self.current_version
            }
        }
    
    def update_status(self, status: ProjectStatus):
        """更新项目状态"""
        self.status = status
        self.updated_at = datetime.now().isoformat()
    
    def save_content(self, content_type: str, content: any):
        """保存内容"""
        if content_type == "idea_requirement":
            self.idea_requirement = content
        elif content_type == "requirement_details":
            self.requirement_details = content
        elif content_type == "world_view":
            self.world_view = content
        elif content_type == "character_profiles":
            self.character_profiles = content
        elif content_type == "core_outline":
            self.core_outline = content
        elif content_type == "script_content":
            self.script_content = content
            self.current_version += 1
            self.script_history.append({
                "version": self.current_version,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
        
        self.updated_at = datetime.now().isoformat()


class ProjectManager:
    """项目管理器"""
    
    def __init__(self, storage_path: str = "assets/projects.json"):
        self.storage_path = storage_path
        self.projects: Dict[str, ScriptProject] = {}
        self.load_projects()
    
    def load_projects(self):
        """从文件加载项目"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 重建项目对象
                for proj_data in data.get("projects", []):
                    proj = ScriptProject(
                        name=proj_data["name"],
                        project_type=ProjectType(proj_data["project_type"]),
                        description=proj_data.get("description", ""),
                        creator=proj_data.get("creator", "user")
                    )
                    proj.project_id = proj_data["project_id"]
                    proj.status = ProjectStatus(proj_data["status"])
                    proj.created_at = proj_data["created_at"]
                    proj.updated_at = proj_data["updated_at"]
                    
                    # 加载内容
                    content = proj_data.get("content", {})
                    proj.idea_requirement = content.get("idea_requirement", "")
                    proj.requirement_details = content.get("requirement_details", {})
                    proj.current_version = content.get("current_version", 0)
                    
                    self.projects[proj.project_id] = proj
                    
        except Exception as e:
            print(f"加载项目失败: {str(e)}")
    
    def save_projects(self):
        """保存项目到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            
            data = {
                "projects": [proj.to_dict() for proj in self.projects.values()],
                "total_count": len(self.projects),
                "updated_at": datetime.now().isoformat()
            }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存项目失败: {str(e)}")
    
    def create_project(
        self,
        name: str,
        project_type: ProjectType,
        description: str = ""
    ) -> ScriptProject:
        """创建新项目"""
        project = ScriptProject(name, project_type, description)
        self.projects[project.project_id] = project
        self.save_projects()
        return project
    
    def get_project(self, project_id: str) -> Optional[ScriptProject]:
        """获取项目"""
        return self.projects.get(project_id)
    
    def list_projects(
        self,
        status: Optional[ProjectStatus] = None,
        project_type: Optional[ProjectType] = None
    ) -> List[ScriptProject]:
        """列出项目"""
        projects = list(self.projects.values())
        
        if status:
            projects = [p for p in projects if p.status == status]
        
        if project_type:
            projects = [p for p in projects if p.project_type == project_type]
        
        return projects
    
    def delete_project(self, project_id: str) -> bool:
        """删除项目"""
        if project_id in self.projects:
            del self.projects[project_id]
            self.save_projects()
            return True
        return False
    
    def update_project(
        self,
        project_id: str,
        **kwargs
    ) -> Optional[ScriptProject]:
        """更新项目"""
        project = self.projects.get(project_id)
        if not project:
            return None
        
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        project.updated_at = datetime.now().isoformat()
        self.save_projects()
        return project


# 导入 os
import os


def create_project_manager() -> ProjectManager:
    """创建项目管理器实例"""
    return ProjectManager()
