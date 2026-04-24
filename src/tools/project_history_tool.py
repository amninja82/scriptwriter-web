#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目历史管理工具
支持项目对话历史保存、加载、跨项目搜索
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from langchain.tools import tool
from coze_coding_dev_sdk import (
    KnowledgeClient,
    Config,
    KnowledgeDocument,
    DataSourceType,
    ChunkConfig
)
from coze_coding_utils.log.write_log import request_context
from utils.project_manager import ProjectManager, ProjectType

# 初始化知识库客户端
def get_knowledge_client():
    """获取知识库客户端"""
    ctx = request_context.get()
    config = Config()
    return KnowledgeClient(config=config, ctx=ctx)


def get_project_history_dataset(project_id: str) -> str:
    """获取项目历史数据集名称"""
    return f"project_history_{project_id}"


@tool
def save_conversation_to_project(project_id: str, conversation: List[Dict]) -> str:
    """
    保存对话到项目历史知识库

    Args:
        project_id: 项目ID
        conversation: 对话列表，每项包含 {"role": "user/assistant", "content": "内容", "timestamp": "时间"}

    Returns:
        保存结果
    """
    try:
        client = get_knowledge_client()
        dataset_name = get_project_history_dataset(project_id)

        # 将对话转换为文本格式存储
        conversation_text = "# 项目对话历史\n\n"
        for msg in conversation:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", datetime.now().isoformat())
            conversation_text += f"## {role} ({timestamp})\n{content}\n\n"

        # 创建文档
        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=conversation_text,
            metadata={
                "project_id": project_id,
                "timestamp": datetime.now().isoformat(),
                "message_count": len(conversation)
            }
        )

        # 上传到知识库
        response = client.add_documents(
            documents=[doc],
            table_name=dataset_name,
            chunk_config=ChunkConfig(separator="\n\n", max_tokens=2000)
        )

        if response.code == 0:
            return f"✅ 成功保存 {len(conversation)} 条对话到项目历史，文档ID: {response.doc_ids}"
        else:
            return f"❌ 保存失败: {response.msg}"

    except Exception as e:
        return f"❌ 保存对话时出错: {str(e)}"


def _load_project_history_impl(project_id: str, limit: int = 20) -> str:
    """
    加载项目历史对话（内部实现函数，供多个工具调用）

    Args:
        project_id: 项目ID
        limit: 返回的对话数量限制

    Returns:
        项目历史对话内容
    """
    try:
        client = get_knowledge_client()
        dataset_name = get_project_history_dataset(project_id)

        # 搜索项目历史
        response = client.search(
            query="项目对话历史",
            table_names=[dataset_name],
            top_k=1,
            min_score=0.0
        )

        if response.code == 0 and len(response.chunks) > 0:
            content = response.chunks[0].content
            # 返回历史对话内容
            return f"📜 **项目历史对话（最近 {limit} 条）**\n\n{content}"
        else:
            return f"⚠️ 未找到项目 {project_id} 的历史对话记录"

    except Exception as e:
        return f"❌ 加载历史对话时出错: {str(e)}"


@tool
def load_project_history(project_id: str, limit: int = 20) -> str:
    """
    加载项目历史对话

    Args:
        project_id: 项目ID
        limit: 返回的对话数量限制

    Returns:
        项目历史对话内容
    """
    return _load_project_history_impl(project_id, limit)


@tool
def search_all_projects(query: str, top_k: int = 5) -> str:
    """
    搜索所有项目的历史对话

    Args:
        query: 搜索关键词
        top_k: 返回结果数量

    Returns:
        搜索结果列表
    """
    try:
        client = get_knowledge_client()

        # 获取所有项目
        pm = ProjectManager()
        projects = pm.list_projects()

        if not projects:
            return "⚠️ 当前没有任何项目"

        # 搜索所有项目的历史数据集
        results = []
        for project in projects:
            dataset_name = get_project_history_dataset(project.project_id)
            try:
                response = client.search(
                    query=query,
                    table_names=[dataset_name],
                    top_k=2,  # 每个项目取2个结果
                    min_score=0.3
                )

                if response.code == 0 and len(response.chunks) > 0:
                    for chunk in response.chunks:
                        results.append({
                            "project_name": project.name,
                            "project_id": project.project_id,
                            "score": chunk.score,
                            "content": chunk.content[:500]  # 截取前500字符
                        })
            except Exception as e:
                # 某个项目可能还没有历史数据集，跳过
                continue

        # 按相关性排序
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:top_k]

        # 格式化结果
        if not results:
            return f"🔍 未找到与「{query}」相关的内容"

        output = f"🔍 **搜索「{query}」的结果**（共找到 {len(results)} 条）\n\n"
        for i, result in enumerate(results, 1):
            output += f"### {i}. {result['project_name']}\n"
            output += f"- 项目ID: `{result['project_id']}`\n"
            output += f"- 相关度: {result['score']:.2f}\n"
            output += f"- 内容摘要: {result['content']}...\n\n"

        return output

    except Exception as e:
        return f"❌ 搜索项目历史时出错: {str(e)}"


@tool
def search_project(project_id: str, query: str, top_k: int = 5) -> str:
    """
    搜索特定项目的历史对话

    Args:
        project_id: 项目ID
        query: 搜索关键词
        top_k: 返回结果数量

    Returns:
        搜索结果
    """
    try:
        client = get_knowledge_client()
        dataset_name = get_project_history_dataset(project_id)

        # 搜索特定项目
        response = client.search(
            query=query,
            table_names=[dataset_name],
            top_k=top_k,
            min_score=0.3
        )

        if response.code == 0 and len(response.chunks) > 0:
            output = f"🔍 **在项目中搜索「{query}」**（共找到 {len(response.chunks)} 条）\n\n"
            for i, chunk in enumerate(response.chunks, 1):
                output += f"### {i}. 相关内容片段\n"
                output += f"- 相关度: {chunk.score:.2f}\n"
                output += f"- 内容: {chunk.content[:800]}...\n\n"
            return output
        else:
            return f"⚠️ 在项目 {project_id} 中未找到与「{query}」相关的内容"

    except Exception as e:
        return f"❌ 搜索项目历史时出错: {str(e)}"


@tool
def switch_to_project(project_id: str) -> str:
    """
    切换到指定项目并加载历史对话

    Args:
        project_id: 项目ID

    Returns:
        切换结果和项目历史
    """
    try:
        # 1. 获取项目信息
        pm = ProjectManager()
        project = pm.get_project(project_id)

        if not project:
            return f"❌ 未找到项目ID: {project_id}"

        # 2. 加载项目历史
        history = _load_project_history_impl(project_id)

        # 3. 返回切换结果
        output = f"✅ **已切换到项目**\n\n"
        output += f"- **项目名称**: {project.name}\n"
        output += f"- **项目类型**: {project.project_type.value}\n"
        output += f"- **项目状态**: {project.status.value}\n"
        output += f"- **创建时间**: {project.created_at}\n"
        output += f"- **最后修改**: {project.updated_at}\n\n"
        output += "---\n\n"
        output += history

        return output

    except Exception as e:
        return f"❌ 切换项目时出错: {str(e)}"


@tool
def get_project_summary(project_id: str) -> str:
    """
    获取项目摘要信息

    Args:
        project_id: 项目ID

    Returns:
        项目摘要
    """
    try:
        pm = ProjectManager()
        project = pm.get_project(project_id)

        if not project:
            return f"❌ 未找到项目ID: {project_id}"

        output = f"📋 **项目摘要**\n\n"
        output += f"- **名称**: {project.name}\n"
        output += f"- **类型**: {project.project_type.value}\n"
        output += f"- **状态**: {project.status.value}\n"
        output += f"- **创建时间**: {project.created_at}\n"
        output += f"- **最后修改**: {project.updated_at}\n\n"

        # 项目内容摘要
        if project.idea_requirement or project.core_outline or project.genre_positioning:
            output += "**项目内容摘要**:\n\n"
            if project.idea_requirement:
                output += f"- **创意描述**: {project.idea_requirement[:200]}...\n"
            if project.requirement_details.get("genre"):
                output += f"- **题材**: {project.requirement_details['genre']}\n"
            if project.core_outline:
                output += f"- **大纲**: {project.core_outline[:200]}...\n"

        # 搜索最近的对话
        history_summary = _load_project_history_impl(project_id, limit=5)
        if "未找到" not in history_summary:
            output += "\n---\n\n"
            output += "📜 **最近的对话**:\n"
            # 只显示第一段摘要
            lines = history_summary.split('\n')[:10]
            output += '\n'.join(lines) + "\n..."

        return output

    except Exception as e:
        return f"❌ 获取项目摘要时出错: {str(e)}"
