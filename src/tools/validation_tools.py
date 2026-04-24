"""
校验工具集
包含人设一致性、剧情逻辑、合规性、格式校验工具
"""
from langchain.tools import tool
from typing import Dict, List, Any
import json


@tool
def consistency_check(script_content: str, character_profiles: str) -> str:
    """
    人设一致性校验
    
    参数:
        script_content: 剧本内容
        character_profiles: 人物档案（JSON 格式字符串）
    
    返回:
        校验报告，包含一致性问题和建议
    """
    try:
        # 解析人物档案
        profiles = json.loads(character_profiles) if isinstance(character_profiles, str) else character_profiles
        
        report = {
            "check_type": "人设一致性校验",
            "status": "通过",
            "issues": [],
            "suggestions": []
        }
        
        # 检查每个角色
        for profile in profiles:
            character_name = profile.get("name", "未知角色")
            personality = profile.get("personality", "")
            background = profile.get("background", "")
            
            # 检查剧本中是否出现该角色
            if character_name not in script_content:
                report["issues"].append({
                    "character": character_name,
                    "issue": f"角色 {character_name} 在剧本中未出现"
                })
            else:
                # 检查性格一致性（简化版）
                report["suggestions"].append({
                    "character": character_name,
                    "suggestion": f"请检查角色 {character_name} 的言行是否符合其性格设定"
                })
        
        if report["issues"]:
            report["status"] = "不通过"
        
        return json.dumps(report, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_report = {
            "check_type": "人设一致性校验",
            "status": "校验失败",
            "error": str(e)
        }
        return json.dumps(error_report, ensure_ascii=False, indent=2)


@tool
def logic_check(script_content: str, outline: str) -> str:
    """
    剧情逻辑校验
    
    参数:
        script_content: 剧本内容
        outline: 大纲内容
    
    返回:
        校验报告，包含逻辑问题和建议
    """
    try:
        report = {
            "check_type": "剧情逻辑校验",
            "status": "通过",
            "issues": [],
            "suggestions": []
        }
        
        # 检查剧本是否符合大纲
        if outline and "情节" in outline:
            # 简化版检查
            report["suggestions"].append({
                "type": "大纲一致性",
                "suggestion": "请检查剧本情节是否与大纲设定一致"
            })
        
        # 检查剧情连贯性
        if len(script_content) < 100:
            report["issues"].append({
                "type": "内容过短",
                "issue": "剧本内容过短，可能缺乏完整情节"
            })
        
        # 检查冲突设置
        if "冲突" not in script_content and "矛盾" not in script_content:
            report["suggestions"].append({
                "type": "冲突设置",
                "suggestion": "建议增加剧情冲突，增强戏剧张力"
            })
        
        if report["issues"]:
            report["status"] = "不通过"
        
        return json.dumps(report, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_report = {
            "check_type": "剧情逻辑校验",
            "status": "校验失败",
            "error": str(e)
        }
        return json.dumps(error_report, ensure_ascii=False, indent=2)


@tool
def compliance_check(script_content: str, genre: str = "一般题材") -> str:
    """
    合规性校验
    
    参数:
        script_content: 剧本内容
        genre: 题材类型
    
    返回:
        校验报告，包含合规性问题和建议
    """
    try:
        report = {
            "check_type": "合规性校验",
            "status": "通过",
            "issues": [],
            "suggestions": []
        }
        
        # 敏感词检查（简化版）
        sensitive_keywords = ["暴力", "色情", "政治敏感"]
        for keyword in sensitive_keywords:
            if keyword in script_content:
                report["issues"].append({
                    "type": "敏感内容",
                    "issue": f"剧本中包含可能敏感的内容: {keyword}",
                    "suggestion": f"建议修改涉及 {keyword} 的内容"
                })
        
        # 题材合规性提示
        genre_compliance = {
            "历史题材": "请检查历史事件和人物描述的准确性",
            "现实题材": "请确保符合社会主义核心价值观",
            "科幻题材": "请确保科学设定合理，避免伪科学"
        }
        
        if genre in genre_compliance:
            report["suggestions"].append({
                "type": "题材合规",
                "suggestion": genre_compliance[genre]
            })
        
        if report["issues"]:
            report["status"] = "需修改"
        
        return json.dumps(report, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_report = {
            "check_type": "合规性校验",
            "status": "校验失败",
            "error": str(e)
        }
        return json.dumps(error_report, ensure_ascii=False, indent=2)


@tool
def format_check(script_content: str, format_type: str = "standard") -> str:
    """
    格式标准化校验
    
    参数:
        script_content: 剧本内容
        format_type: 格式类型 (standard, detailed, simplified)
    
    返回:
        校验报告，包含格式问题和建议
    """
    try:
        report = {
            "check_type": "格式标准化校验",
            "status": "通过",
            "issues": [],
            "suggestions": []
        }
        
        # 检查场景格式
        if "场景" not in script_content and "场" not in script_content:
            report["issues"].append({
                "type": "场景格式",
                "issue": "剧本中缺少场景标识",
                "suggestion": "请使用标准场景格式，如 '第1场 日/内/地点'"
            })
        
        # 检查人物对话格式
        if "（" in script_content and "）" in script_content:
            report["suggestions"].append({
                "type": "对话格式",
                "suggestion": "请使用标准对话格式，人物名后应使用括号标注动作或情感"
            })
        else:
            report["issues"].append({
                "type": "对话格式",
                "issue": "对话格式不完整，建议使用括号标注人物动作或情感"
            })
        
        # 检查时间、地点标注
        if "日" not in script_content and "夜" not in script_content:
            report["suggestions"].append({
                "type": "时间标注",
                "suggestion": "建议在场景中标注时间（日/夜/晨/昏）"
            })
        
        if report["issues"]:
            report["status"] = "需调整"
        
        return json.dumps(report, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_report = {
            "check_type": "格式标准化校验",
            "status": "校验失败",
            "error": str(e)
        }
        return json.dumps(error_report, ensure_ascii=False, indent=2)
