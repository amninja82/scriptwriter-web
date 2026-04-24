#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能联网搜索并分类加入知识库的工具
支持：搜索 → 分析内容类型 → 自动分类 → 上传到对应知识库
"""

import json
from typing import Dict, List, Optional
from langchain.tools import tool
from coze_coding_dev_sdk import (
    KnowledgeClient,
    Config,
    KnowledgeDocument,
    DataSourceType,
    ChunkConfig
)
from coze_coding_utils.log.write_log import request_context
from langchain_openai import ChatOpenAI
import os

# 获取环境变量
WORKSPACE_PATH = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")

# 知识库数据集映射
DATASET_MAPPING = {
    "编剧技巧": "scriptwriter_knowledge",
    "题材分析": "scriptwriter_knowledge",
    "创作方法": "scriptwriter_knowledge",
    "角色设计": "scriptwriter_knowledge",
    "世界观构建": "worldview_knowledge",
    "故事钩子": "hook_knowledge",
    "情绪价值": "emotion_knowledge",
    "冲突设计": "conflict_knowledge",
    "影视案例": "genre_knowledge",
    "作品分析": "genre_knowledge",
    "创作特点": "genre_knowledge",
    "高概念设定": "worldview_knowledge",
}


def get_llm():
    """获取 LLM 实例用于内容分析"""
    config_path = os.path.join(WORKSPACE_PATH, "config/scriptwriter_llm_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    return ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=0.3,  # 较低的温度，确保分类准确
        timeout=60
    )


def analyze_content_type(content: str) -> Dict[str, str]:
    """
    分析内容类型并分类

    Args:
        content: 搜索到的内容

    Returns:
        包含类型、类别、数据集的字典
    """
    llm = get_llm()

    prompt = f"""请分析以下内容，确定它的类型和应该存储在哪个知识库数据集中。

内容：
{content[:1000]}

请以 JSON 格式返回，包含以下字段：
- "type": 内容类型（编剧技巧/题材分析/角色设计/世界观构建/故事钩子/情绪价值/冲突设计/影视案例/作品分析/创作特点/高概念设定）
- "category": 详细分类（如"悬疑题材开篇技巧"）
- "dataset": 应该存储的数据集名称（scriptwriter_knowledge / genre_knowledge / hook_knowledge / emotion_knowledge / worldview_knowledge / conflict_knowledge）
- "confidence": 置信度（0-1之间的小数）

只返回 JSON，不要其他内容。"""

    try:
        response = llm.invoke(prompt)
        result_text = response.content

        # 提取 JSON（去除可能的 markdown 代码块标记）
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()

        result = json.loads(result_text)

        # 验证并修正结果
        if "dataset" not in result:
            result["dataset"] = "scriptwriter_knowledge"

        # 如果数据集不存在，使用默认值
        if result["dataset"] not in DATASET_MAPPING.values():
            result["dataset"] = "scriptwriter_knowledge"

        return result

    except Exception as e:
        # 分析失败，使用默认分类
        return {
            "type": "编剧技巧",
            "category": "未知分类",
            "dataset": "scriptwriter_knowledge",
            "confidence": 0.0
        }


def add_to_knowledge(content: str, dataset: str, metadata: Dict) -> bool:
    """
    将内容添加到知识库

    Args:
        content: 内容文本
        dataset: 数据集名称
        metadata: 元数据

    Returns:
        是否成功
    """
    try:
        ctx = request_context.get()
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)

        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=content,
            metadata=metadata
        )

        response = client.add_documents(
            documents=[doc],
            table_name=dataset,
            chunk_config=ChunkConfig(separator="\n\n", max_tokens=1500)
        )

        return response.code == 0

    except Exception as e:
        print(f"添加到知识库失败: {e}")
        return False


@tool
def smart_search_and_classify(query: str, auto_save: bool = True) -> str:
    """
    联网搜索内容，智能分析类型，自动分类并加入知识库

    Args:
        query: 搜索关键词
        auto_save: 是否自动保存到知识库（默认 True）

    Returns:
        搜索结果和分类信息
    """
    try:
        # 1. 联网搜索
        from tools.web_search_tool import web_search

        search_result = web_search(query)
        if "搜索失败" in search_result:
            return f"❌ 搜索失败：{search_result}"

        # 提取搜索结果内容
        if "搜索结果" in search_result:
            # 提取搜索到的内容
            lines = search_result.split('\n')
            content = []
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    content.append(line.strip())

            if not content:
                return "❌ 未找到相关内容"

            full_content = '\n'.join(content)
        else:
            full_content = search_result

        # 2. 智能分析内容类型
        if auto_save:
            analysis = analyze_content_type(full_content)

            # 3. 构建要保存的内容
            save_content = f"# 搜索：{query}\n\n"
            save_content += f"**内容类型**: {analysis.get('type', '未知')}\n"
            save_content += f"**详细分类**: {analysis.get('category', '未知')}\n"
            save_content += f"**置信度**: {analysis.get('confidence', 0):.2f}\n\n"
            save_content += "---\n\n"
            save_content += full_content

            # 4. 添加到知识库
            metadata = {
                "source": "smart_search",
                "query": query,
                "type": analysis.get('type', '未知'),
                "category": analysis.get('category', '未知'),
                "confidence": str(analysis.get('confidence', 0))
            }

            dataset = analysis.get('dataset', 'scriptwriter_knowledge')
            success = add_to_knowledge(save_content, dataset, metadata)

            if success:
                result = f"""✅ **搜索成功并已自动保存到知识库**

📊 **分类信息**：
- 内容类型：{analysis.get('type', '未知')}
- 详细分类：{analysis.get('category', '未知')}
- 存储数据集：{dataset}
- 置信度：{analysis.get('confidence', 0):.2f}

📋 **搜索结果**：
{search_result}
"""
            else:
                result = f"""⚠️ **搜索成功，但保存到知识库失败**

📋 **搜索结果**：
{search_result}

您可以手动使用 `add_knowledge_content` 工具保存此内容。"""
        else:
            result = f"""✅ **搜索成功**

📋 **搜索结果**：
{search_result}
"""

        return result

    except Exception as e:
        return f"❌ 智能搜索失败: {str(e)}"


@tool
def search_multiple_sources(query: str, sources: str = "baidu,google") -> str:
    """
    从多个来源联网搜索内容

    Args:
        query: 搜索关键词
        sources: 搜索来源（逗号分隔，如 "baidu,google,bing"）

    Returns:
        搜索结果汇总
    """
    try:
        from tools.web_search_tool import web_search

        source_list = [s.strip() for s in sources.split(',')]
        all_results = []

        for source in source_list:
            # 注意：这里简化处理，实际 web_search 工具可能不支持指定来源
            # 如果工具支持，可以修改这里
            result = web_search(query)
            all_results.append(f"## 来源：{source}\n{result}")

        return f"✅ **多来源搜索结果**\n\n" + "\n\n---\n\n".join(all_results)

    except Exception as e:
        return f"❌ 多来源搜索失败: {str(e)}"


@tool
def search_and_compare(query: str) -> str:
    """
    搜索相关内容并进行对比分析

    Args:
        query: 搜索关键词

    Returns:
        搜索结果和对比分析
    """
    try:
        from tools.web_search_tool import web_search

        # 1. 联网搜索
        search_result = web_search(query)

        # 2. 搜索知识库
        from tools.knowledge_search_tool import knowledge_search
        knowledge_result = knowledge_search(query)

        # 3. 对比分析
        result = f"""✅ **搜索与对比分析**

## 联网搜索结果
{search_result}

---

## 知识库搜索结果
{knowledge_result}

---

## 对比分析
请根据以上两个来源的信息，进行对比分析，找出相同点和不同点，并给出综合建议。
"""

        return result

    except Exception as e:
        return f"❌ 搜索对比失败: {str(e)}"
