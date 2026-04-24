"""
多智能体编剧系统 - 主入口
整合 LangGraph 状态机和所有 Agent
"""
import os
import json
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage

from graphs.scriptwriter_state import ScriptWriterState
from graphs.scriptwriter_graph import create_scriptwriter_graph
from tools.knowledge_search_tool import add_to_knowledge_base
from tools.web_search_tool import web_search_and_save


class ScriptWriterSystem:
    """多智能体编剧系统主类"""
    
    def __init__(self):
        """初始化编剧系统"""
        self.graph = create_scriptwriter_graph()
        self.state = {
            "messages": [],
            "user_requirement": "",
            "parsed_requirement": {},
            "genre_positioning": {},
            "audience_profile": {},
            "world_view": "",
            "character_profiles": [],
            "core_outline": "",
            "episode_outlines": [],
            "script_content": "",
            "validation_reports": [],
            "foreshadowings": [],
            "current_version": 0,
            "script_history": [],
            "modification_requests": [],
            "current_stage": "初始化",
            "is_valid": True,
            "metadata": {},
            "checkpoint_data": None
        }
    
    def create_script(self, user_requirement: str) -> dict:
        """
        创建剧本
        
        参数:
            user_requirement: 用户需求描述
        
        返回:
            剧本创作结果
        """
        print("=" * 60)
        print("🎬 多智能体编剧系统启动")
        print("=" * 60)
        
        # 初始化状态
        self.state["user_requirement"] = user_requirement
        self.state["messages"] = [HumanMessage(content=user_requirement)]
        
        print(f"\n用户需求: {user_requirement}")
        print("\n开始创作流程...\n")
        
        try:
            # 执行工作流
            result = self.graph.invoke(self.state)
            
            # 整理结果
            output = {
                "success": True,
                "requirement": user_requirement,
                "parsed_requirement": result.get("parsed_requirement", ""),
                "genre_positioning": result.get("genre_positioning", ""),
                "world_view": result.get("world_view", ""),
                "character_profiles": result.get("character_profiles", []),
                "core_outline": result.get("core_outline", ""),
                "episode_outlines": result.get("episode_outlines", []),
                "script_content": result.get("script_content", ""),
                "validation_reports": result.get("validation_reports", []),
                "current_version": result.get("current_version", 1),
                "current_stage": result.get("current_stage", ""),
                "messages": [msg.content for msg in result.get("messages", [])]
            }
            
            print("\n" + "=" * 60)
            print("✅ 剧本创作完成！")
            print("=" * 60)
            print(f"\n当前阶段: {output['current_stage']}")
            print(f"当前版本: v{output['current_version']}")
            
            return output
            
        except Exception as e:
            print(f"\n❌ 创作过程出错: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_knowledge(self, content: str, dataset: str = "scriptwriter_knowledge") -> dict:
        """
        添加内容到知识库
        
        参数:
            content: 内容文本
            dataset: 知识库名称
        
        返回:
            添加结果
        """
        print(f"\n📚 正在添加内容到知识库: {dataset}")
        result = add_to_knowledge_base.invoke(content=content, dataset=dataset)
        return {"result": result}
    
    def search_knowledge(self, query: str, dataset: str = "scriptwriter_knowledge") -> dict:
        """
        搜索知识库
        
        参数:
            query: 搜索关键词
            dataset: 知识库名称
        
        返回:
            搜索结果
        """
        from tools.scriptwriter_tools import knowledge_search
        
        print(f"\n🔍 正在搜索知识库: {query}")
        result = knowledge_search.invoke(query=query, dataset=dataset)
        return {"result": result}
    
    def web_search_and_save(self, query: str, dataset: str = "scriptwriter_knowledge") -> dict:
        """
        搜索网络并保存到知识库
        
        参数:
            query: 搜索关键词
            dataset: 目标知识库名称
        
        返回:
            搜索和保存结果
        """
        print(f"\n🌐 正在搜索网络并保存: {query}")
        result = web_search_and_save.invoke(query=query, dataset=dataset)
        return {"result": result}
    
    def modify_script(self, modification_requests: list) -> dict:
        """
        修改剧本
        
        参数:
            modification_requests: 修改意见列表
        
        返回:
            修改结果
        """
        print("\n🔄 正在修改剧本...")
        print(f"修改意见: {modification_requests}")
        
        # 更新状态中的修改请求
        self.state["modification_requests"] = modification_requests
        self.state["messages"] = self.state.get("messages", [])
        
        try:
            # 执行修改节点
            result = self.graph.invoke(self.state)
            
            return {
                "success": True,
                "script_content": result.get("script_content", ""),
                "current_version": result.get("current_version", 1),
                "current_stage": result.get("current_stage", "")
            }
            
        except Exception as e:
            print(f"\n❌ 修改过程出错: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


def create_scriptwriter_system():
    """
    创建编剧系统实例
    
    返回:
        ScriptWriterSystem 实例
    """
    return ScriptWriterSystem()


# 便捷函数
def create_script(user_requirement: str) -> dict:
    """
    快速创建剧本
    
    参数:
        user_requirement: 用户需求
    
    返回:
        剧本创作结果
    """
    system = create_scriptwriter_system()
    return system.create_script(user_requirement)


if __name__ == "__main__":
    # 测试示例
    print("多智能体编剧系统测试\n")
    
    test_requirement = """
    请创作一部古代宫廷悬疑剧，共10集。
    核心看点：宫廷阴谋、破案推理、女医成长。
    对标作品：《大宋提刑官》《琅琊榜》。
    受众：25-40岁女性，喜欢古装悬疑。
    """
    
    system = create_scriptwriter_system()
    result = system.create_script(test_requirement)
    
    print("\n\n" + "=" * 60)
    print("创作结果摘要")
    print("=" * 60)
    print(f"成功: {result.get('success')}")
    print(f"阶段: {result.get('current_stage')}")
    print(f"版本: v{result.get('current_version')}")
