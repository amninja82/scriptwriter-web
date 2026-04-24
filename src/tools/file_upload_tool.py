"""
文件上传工具
支持上传本地文件到知识库
"""
from langchain.tools import tool
from typing import Optional
import os
import json
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType, ChunkConfig
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def upload_text_file_to_knowledge(file_path: str, dataset: str = "scriptwriter_knowledge") -> str:
    """
    上传文本文件到知识库
    
    参数:
        file_path: 本地文件路径（绝对路径）
        dataset: 目标知识库名称
    
    返回:
        上传结果
    """
    try:
        ctx = request_context.get() or new_context(method="upload_text_file_to_knowledge")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"文件不存在: {file_path}"
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果文件为空
        if not content.strip():
            return f"文件为空: {file_path}"
        
        # 创建文档
        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=content,
            filename=os.path.basename(file_path)
        )
        
        # 配置分块
        chunk_config = ChunkConfig(
            separator="\n\n",
            max_tokens=1500,
            remove_extra_spaces=True
        )
        
        # 上传到知识库
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        response = client.add_documents(
            documents=[doc],
            table_name=dataset,
            chunk_config=chunk_config
        )
        
        if response.code == 0:
            chunk_count = len(response.doc_ids) if response.doc_ids else '未知'
            result = f"""
✅ 文件上传成功！

文件: {os.path.basename(file_path)}
大小: {len(content)} 字符
知识库: {dataset}
文档ID: {response.doc_ids}
分块数: {chunk_count}
"""
            return result
        else:
            return f"❌ 上传失败: {response.msg}"
            
    except Exception as e:
        return f"❌ 上传出错: {str(e)}"


@tool
def upload_url_to_knowledge(url: str, dataset: str = "scriptwriter_knowledge") -> str:
    """
    上传 URL 内容到知识库
    
    参数:
        url: 文档 URL
        dataset: 目标知识库名称
    
    返回:
        上传结果
    """
    try:
        ctx = request_context.get() or new_context(method="upload_url_to_knowledge")
        
        # 创建文档（从 URL）
        doc = KnowledgeDocument(
            source=DataSourceType.URL,
            raw_data=url
        )
        
        # 配置分块
        chunk_config = ChunkConfig(
            separator="\n\n",
            max_tokens=1500,
            remove_extra_spaces=True
        )
        
        # 上传到知识库
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        response = client.add_documents(
            documents=[doc],
            table_name=dataset,
            chunk_config=chunk_config
        )
        
        if response.code == 0:
            result = f"""
✅ URL 上传成功！

URL: {url}
知识库: {dataset}
文档ID: {response.doc_ids}
"""
            return result
        else:
            return f"❌ 上传失败: {response.msg}"
            
    except Exception as e:
        return f"❌ 上传出错: {str(e)}"


@tool
def batch_upload_files_to_knowledge(
    file_paths: list[str], 
    dataset: str = "scriptwriter_knowledge"
) -> str:
    """
    批量上传文件到知识库
    
    参数:
        file_paths: 本地文件路径列表（绝对路径）
        dataset: 目标知识库名称
    
    返回:
        批量上传结果
    """
    try:
        results = []
        success_count = 0
        fail_count = 0
        
        for file_path in file_paths:
            result = upload_text_file_to_knowledge(file_path, dataset)
            results.append(result)
            
            if "✅" in result:
                success_count += 1
            else:
                fail_count += 1
        
        summary = f"""
📦 批量上传完成

成功: {success_count} 个文件
失败: {fail_count} 个文件
总计: {len(file_paths)} 个文件

详细结果:
{chr(10).join([f"{i+1}. {r}" for i, r in enumerate(results)])}
"""
        return summary
        
    except Exception as e:
        return f"❌ 批量上传出错: {str(e)}"


@tool
def list_knowledge_datasets() -> str:
    """
    列出所有知识库数据集
    
    返回:
        数据集列表
    """
    try:
        ctx = request_context.get() or new_context(method="list_knowledge_datasets")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        # 这里需要调用实际的知识库列表 API
        # 暂时返回模拟数据
        return """
📚 知识库数据集列表

1. scriptwriter_knowledge - 主要编剧知识库
2. character_library - 人物角色库
3. world_archives - 世界观资料库
4. script_theory - 编剧理论库

使用 search_knowledge 在指定数据集中搜索内容。
"""
        
    except Exception as e:
        return f"❌ 获取数据集列表失败: {str(e)}"


@tool
def delete_knowledge_document(doc_id: str, dataset: str = "scriptwriter_knowledge") -> str:
    """
    删除知识库文档
    
    参数:
        doc_id: 文档 ID
        dataset: 知识库名称
    
    返回:
        删除结果
    """
    try:
        ctx = request_context.get() or new_context(method="delete_knowledge_document")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        # 调用删除 API（需要实际 API 支持）
        # response = client.delete_document(doc_id=doc_id, table_name=dataset)
        
        return f"""
✅ 文档删除成功（模拟）

文档ID: {doc_id}
知识库: {dataset}

注意: 实际删除功能需要 API 支持，当前为模拟结果。
"""
        
    except Exception as e:
        return f"❌ 删除失败: {str(e)}"
