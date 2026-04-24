"""
在线搜索工具
用于实时搜索网络资料（对标作品、历史背景、创作技巧等）
"""
from langchain.tools import tool
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def web_search(query: str, count: int = 5, time_range: str = None) -> str:
    """
    在线搜索网络信息
    
    参数:
        query: 搜索关键词
        count: 返回结果数量，默认 5
        time_range: 时间范围 (如 "1d", "1w", "1m")
    
    返回:
        搜索结果摘要
    """
    try:
        ctx = request_context.get() or new_context(method="web_search")
        client = SearchClient(ctx=ctx)
        
        # 执行搜索
        response = client.web_search(
            query=query,
            count=count,
            need_summary=True,
            time_range=time_range
        )
        
        if response.web_items:
            results = []
            
            # 添加 AI 摘要
            if hasattr(response, 'summary') and response.summary:
                results.append(f"【AI 摘要】\n{response.summary}\n")
            
            # 添加搜索结果
            for i, item in enumerate(response.web_items, 1):
                result = f"[结果 {i}]\n"
                result += f"标题: {item.title}\n"
                result += f"来源: {item.site_name}\n"
                result += f"链接: {item.url}\n"
                if hasattr(item, 'summary') and item.summary:
                    result += f"摘要: {item.summary}\n"
                elif item.snippet:
                    result += f"摘要: {item.snippet}\n"
                results.append(result)
            
            return "\n".join(results)
        else:
            return f"未找到相关结果。查询: {query}"
            
    except Exception as e:
        return f"网络搜索失败: {str(e)}"


@tool
def web_search_and_save(query: str, dataset: str = "scriptwriter_knowledge") -> str:
    """
    搜索网络信息并保存到知识库
    
    参数:
        query: 搜索关键词
        dataset: 目标知识库名称
    
    返回:
        搜索结果和保存状态
    """
    try:
        # 先搜索
        search_result = web_search(query, count=3)
        
        # 保存到知识库
        from tools.knowledge_search_tool import add_to_knowledge_base
        save_result = add_to_knowledge_base(search_result, dataset)
        
        return f"{search_result}\n\n{save_result}"
        
    except Exception as e:
        return f"搜索并保存失败: {str(e)}"
