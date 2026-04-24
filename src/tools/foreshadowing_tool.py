"""
伏笔管理工具
用于记录和检查剧本中的伏笔设置与回收
"""
from langchain.tools import tool
from typing import Dict, List, Any
import json
from datetime import datetime


@tool
def add_foreshadowing(foreshadowing_text: str, foreshadowing_type: str, 
                     planned_recognition: str = "") -> str:
    """
    添加伏笔记录
    
    参数:
        foreshadowing_text: 伏笔内容描述
        foreshadowing_type: 伏笔类型 (物品, 对话, 事件, 人物)
        planned_recognition: 计划回收的位置/场景
    
    返回:
        伏笔添加结果
    """
    try:
        foreshadowing = {
            "id": f"foreshadowing_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "text": foreshadowing_text,
            "type": foreshadowing_type,
            "planned_recognition": planned_recognition,
            "status": "未回收",
            "created_at": datetime.now().isoformat(),
            "recognition_at": None
        }
        
        result = {
            "status": "success",
            "message": "伏笔添加成功",
            "foreshadowing": foreshadowing
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"伏笔添加失败: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@tool
def check_foreshadowing(foreshadowings: str, script_content: str, 
                        current_stage: str = "创作中") -> str:
    """
    检查伏笔回收情况
    
    参数:
        foreshadowings: 伏笔列表（JSON 格式字符串）
        script_content: 剧本内容
        current_stage: 当前创作阶段
    
    返回:
        伏笔回收报告
    """
    try:
        # 解析伏笔列表
        foreshadowing_list = json.loads(foreshadowings) if isinstance(foreshadowings, str) else foreshadowings
        
        report = {
            "check_type": "伏笔回收检查",
            "current_stage": current_stage,
            "total_foreshadowings": len(foreshadowing_list),
            "recognized": 0,
            "not_recognized": 0,
            "status": "通过",
            "details": []
        }
        
        for fs in foreshadowing_list:
            fs_id = fs.get("id", "unknown")
            fs_text = fs.get("text", "")
            planned = fs.get("planned_recognition", "")
            
            # 检查是否已回收
            is_recognized = False
            if fs.get("status") == "已回收":
                is_recognized = True
                report["recognized"] += 1
            elif fs_text in script_content and planned in script_content:
                # 如果伏笔内容和计划回收位置都在剧本中出现，标记为可能已回收
                report["details"].append({
                    "id": fs_id,
                    "text": fs_text,
                    "status": "可能已回收",
                    "note": f"请确认是否在 '{planned}' 处完成回收"
                })
                report["not_recognized"] += 1
            else:
                report["not_recognized"] += 1
                report["details"].append({
                    "id": fs_id,
                    "text": fs_text,
                    "status": "未回收",
                    "planned_location": planned if planned else "未指定"
                })
        
        # 根据未回收伏笔数量判断状态
        if current_stage == "终稿" and report["not_recognized"] > 0:
            report["status"] = "需完善"
            report["warning"] = "终稿阶段仍有伏笔未回收，建议补充"
        
        return json.dumps(report, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_report = {
            "check_type": "伏笔回收检查",
            "status": "检查失败",
            "error": str(e)
        }
        return json.dumps(error_report, ensure_ascii=False, indent=2)


@tool
def update_foreshadowing_status(foreshadowing_id: str, status: str, 
                                 recognition_note: str = "") -> str:
    """
    更新伏笔状态
    
    参数:
        foreshadowing_id: 伏笔 ID
        status: 新状态 (未回收, 已回收, 无效)
        recognition_note: 回收说明
    
    返回:
        更新结果
    """
    try:
        result = {
            "status": "success",
            "message": f"伏笔状态已更新为: {status}",
            "foreshadowing_id": foreshadowing_id,
            "new_status": status,
            "recognition_note": recognition_note
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"更新失败: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)
