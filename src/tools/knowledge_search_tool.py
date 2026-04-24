"""
知识库搜索工具
用于从知识库中检索相关剧本创作资料
"""
from langchain.tools import tool
from coze_coding_dev_sdk import KnowledgeClient, Config, ChunkConfig
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def knowledge_search(query: str, dataset: str = "scriptwriter_knowledge") -> str:
    """
    从编剧知识库中搜索相关信息
    
    参数:
        query: 搜索查询文本
        dataset: 知识库名称，默认为 "scriptwriter_knowledge"
    
    返回:
        搜索结果摘要
    """
    try:
        ctx = request_context.get() or new_context(method="knowledge_search")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        # 执行搜索
        response = client.search(
            query=query,
            table_names=[dataset] if dataset else None,
            top_k=5,
            min_score=0.6
        )
        
        if response.code == 0 and response.chunks:
            results = []
            for i, chunk in enumerate(response.chunks, 1):
                results.append(f"[结果 {i} - 相似度: {chunk.score:.4f}]\n{chunk.content}\n")
            return "\n".join(results)
        else:
            return f"未找到相关内容。查询: {query}"
            
    except Exception as e:
        return f"知识库搜索失败: {str(e)}"


@tool
def add_to_knowledge_base(content: str, dataset: str = "scriptwriter_knowledge") -> str:
    """
    添加内容到编剧知识库
    
    参数:
        content: 要添加的内容文本
        dataset: 目标知识库名称
    
    返回:
        添加结果
    """
    try:
        ctx = request_context.get() or new_context(method="add_to_knowledge_base")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        from coze_coding_dev_sdk import KnowledgeDocument, DataSourceType
        
        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=content
        )
        
        chunk_config = ChunkConfig(
            separator="\n\n",
            max_tokens=1500,
            remove_extra_spaces=True
        )
        
        response = client.add_documents(
            documents=[doc],
            table_name=dataset,
            chunk_config=chunk_config
        )
        
        if response.code == 0:
            return f"成功添加到知识库。文档ID: {response.doc_ids}"
        else:
            return f"添加失败: {response.msg}"
            
    except Exception as e:
        return f"添加到知识库失败: {str(e)}"
