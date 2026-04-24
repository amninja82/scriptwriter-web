#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
上传知识库文档到知识库
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.getenv('COZE_WORKSPACE_PATH', '/workspace/projects'), 'src'))

from coze_coding_dev_sdk import (
    KnowledgeClient,
    Config,
    KnowledgeDocument,
    DataSourceType,
    ChunkConfig
)
from coze_coding_utils.log.write_log import request_context

def upload_file_to_knowledge(file_path, table_name, description=""):
    """上传单个文件到知识库"""
    print(f"\n正在上传: {file_path} -> {table_name}")

    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

    # 初始化客户端
    ctx = request_context.get()  # 优先从请求上下文获取
    config = Config()
    client = KnowledgeClient(config=config, ctx=ctx)
    
    # 配置分块策略
    chunk_config = ChunkConfig(
        separator="\n\n",
        max_tokens=1500,
        remove_extra_spaces=True
    )
    
    # 创建文档对象
    doc = KnowledgeDocument(
        source=DataSourceType.TEXT,
        raw_data=content,
        metadata={"description": description, "source_file": os.path.basename(file_path)}
    )
    
    # 上传文档
    try:
        response = client.add_documents(
            documents=[doc],
            table_name=table_name,
            chunk_config=chunk_config
        )
        
        if response.code == 0:
            print(f"✅ 成功上传 {len(response.doc_ids)} 个文档块")
            print(f"   文档ID: {response.doc_ids}")
            return True
        else:
            print(f"❌ 上传失败: {response.msg}")
            return False
    except Exception as e:
        print(f"❌ 上传异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("开始上传编剧智能体知识库文档")
    print("=" * 60)
    
    # 定义文档列表
    documents = [
        {
            "file": "/tmp/编剧智能体知识库v01.txt",
            "table": "scriptwriter_knowledge",
            "desc": "编剧智能体核心知识库：题材分类、角色设计、世界观、冲突、钩子、情绪价值等"
        },
        {
            "file": "/tmp/不同影视类型的创作特点.txt",
            "table": "genre_knowledge",
            "desc": "7种影视类型（短剧、电视剧、网剧、电影、网大、动画）的创作特点"
        },
        {
            "file": "/tmp/故事钩子.txt",
            "table": "hook_knowledge",
            "desc": "7种故事钩子分类和6大黄金法则"
        },
        {
            "file": "/tmp/深度共情的情绪价值点.txt",
            "table": "emotion_knowledge",
            "desc": "9大类情绪价值点：亲情、爱情、成长、现实困境等"
        },
        {
            "file": "/tmp/世界观与高概念设定.txt",
            "table": "worldview_knowledge",
            "desc": "5类世界观和6类高概念设定的分类与分析"
        },
        {
            "file": "/tmp/戏剧化冲突.txt",
            "table": "conflict_knowledge",
            "desc": "戏剧冲突的4类分类和9大实现手法"
        }
    ]
    
    # 上传所有文档
    success_count = 0
    fail_count = 0
    
    for doc in documents:
        if upload_file_to_knowledge(doc["file"], doc["table"], doc["desc"]):
            success_count += 1
        else:
            fail_count += 1
    
    # 输出总结
    print("\n" + "=" * 60)
    print(f"上传完成！成功: {success_count}, 失败: {fail_count}")
    print("=" * 60)
    
    # 列出所有数据集
    print("\n当前知识库数据集：")
    print("-" * 60)
    for doc in documents:
        print(f"• {doc['table']}: {doc['desc']}")
    
    return fail_count == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
