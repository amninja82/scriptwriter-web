# 多智能体编剧系统 🎬

一个基于 LangGraph 和 CrewAI 的专业剧本创作系统，由 7 个专业智能体协作完成从需求解析到剧本交付的全流程。

## ✨ 核心特性

### 🤖 7 个专业智能体
1. **策划师 Agent** - 需求解析、题材定位、受众分析
2. **世界观架构师 Agent** - 世界观设定构建
3. **人设师 Agent** - 人物档案创建
4. **主笔编剧 Agent** - 大纲创作、剧本正文生成
5. **剧本医生 Agent** - 质量审查、修改建议
6. **合规专员 Agent** - 合规性检查
7. **制片顾问 Agent** - 商业价值评估

### 🔄 9 节点工作流
```
需求解析 → 题材定位 → 世界观与人设 → 核心大纲 → 
大纲校验 → 分集/分场大纲 → 剧本正文生成 → 终稿校验 → 修改迭代
```

### 📚 知识库系统
- 支持导入文档、URL、对象存储文件
- 语义检索能力
- 分类管理（题材库、人设库、场景库等）

### 🔍 在线搜索能力
- 实时搜索网络资料
- 一键保存到知识库
- 智能分类整理

### 🔬 多维度校验
- 人设一致性检查
- 剧情逻辑校验
- 合规性审查
- 格式标准化检查

### 🎯 伏笔管理
- 伏笔时序记录
- 自动回收检查
- 版本追踪

## 📦 项目结构

```
src/
├── agents/                    # Agent 定义
│   ├── agent.py              # 主 Agent 入口
│   ├── scriptwriter_system.py # 编剧系统
│   ├── scriptwriter_agents.py # Agent 集合
│   ├── planner_agent.py      # 策划师
│   ├── worldview_agent.py    # 世界观架构师
│   ├── character_agent.py    # 人设师
│   ├── writer_agent.py       # 主笔编剧
│   └── reviewer_agents.py    # 审查类 Agent
├── tools/                     # 工具定义
│   ├── knowledge_search_tool.py      # 知识库搜索
│   ├── web_search_tool.py             # 在线搜索
│   ├── validation_tools.py            # 校验工具
│   └── foreshadowing_tool.py          # 伏笔管理
├── graphs/                    # LangGraph 图
│   ├── scriptwriter_state.py  # 状态定义
│   └── scriptwriter_graph.py  # 工作流图
└── storage/                   # 存储层
    ├── memory/                # 内存存储
    ├── database/              # 数据库
    └── s3/                    # 对象存储

config/
└── scriptwriter_llm_config.json  # 模型配置

tests/
└── test_scriptwriter.py       # 测试用例
```

## 🚀 快速开始

### 1. 运行测试
```bash
cd /workspace/projects
PYTHONPATH=/workspace/projects/src:$PYTHONPATH python tests/test_scriptwriter.py
```

### 2. 使用编剧系统
```python
from agents.scriptwriter_system import create_scriptwriter_system

# 创建系统
system = create_scriptwriter_system()

# 创作剧本
result = system.create_script("""
    请创作一部古代宫廷悬疑剧，共10集。
    核心看点：宫廷阴谋、破案推理、女医成长。
    对标作品：《大宋提刑官》《琅琊榜》。
    受众：25-40岁女性，喜欢古装悬疑。
""")

# 获取剧本
print(result["script_content"])
```

### 3. 知识库操作
```python
# 添加内容到知识库
system.add_knowledge("三国时期政治制度...", "scriptwriter_knowledge")

# 搜索知识库
result = system.search_knowledge("古代刑法", "scriptwriter_knowledge")
```

### 4. 在线搜索
```python
# 搜索并保存
result = system.web_search_and_save("古代宫廷制度", "scriptwriter_knowledge")
```

## 📋 工作流详解

### 节点1: 需求解析
- 提取核心要素（题材、集数、受众等）
- 生成需求确认清单

### 节点2: 题材定位
- 精确定位剧本类型
- 市场分析和商业价值评估
- 受众画像生成

### 节点3: 世界观与人设
- 构建完整世界观设定
- 创建人物档案
- 定义人物关系

### 节点4: 核心大纲
- 采用三幕式结构
- 标注核心冲突、反转、伏笔
- 定义人物弧光

### 节点5: 大纲校验
- 人设一致性检查
- 剧情逻辑审查
- 合规性初筛

### 节点6: 分集/分场大纲
- 拆解为详细场景
- 定义每场目标和冲突

### 节点7: 剧本正文生成
- 标准剧本格式
- 符合人物设定
- 节奏控制

### 节点8: 终稿校验
- 全面质量检查
- 伏笔回收验证
- 合规性审查

### 节点9: 修改迭代
- 根据反馈修改
- 版本管理
- 持续优化

## 🛠️ 技术栈

- **编排框架**: LangGraph 1.0
- **多智能体**: LangChain Agents
- **大模型**: 豆包 4.0 Ultra (doubao-seed-2-0-pro-260215)
- **知识库**: coze-coding-dev-sdk
- **存储**: PostgreSQL + MemorySaver
- **语言**: Python 3.12

## 📝 注意事项

1. **环境变量**: 确保以下环境变量已设置
   - `COZE_WORKSPACE_PATH`: 项目路径
   - `COZE_WORKLOAD_IDENTITY_API_KEY`: API 密钥
   - `COZE_INTEGRATION_MODEL_BASE_URL`: 模型 API 地址

2. **PYTHONPATH**: 运行时需设置
   ```bash
   PYTHONPATH=/workspace/projects/src:$PYTHONPATH
   ```

3. **知识库**: 默认数据集名为 `scriptwriter_knowledge`

4. **测试状态**: 当前使用 MemorySaver，重启后数据不持久化

## 🎯 适用场景

- 影视编剧工作室
- 内容创作团队
- 个人编剧辅助
- 剧本创作教学
- 影视项目开发

## 📊 系统优势

✅ **专业协作**: 7 个智能体分工明确，各司其职
✅ **全流程覆盖**: 从需求到终稿完整闭环
✅ **质量控制**: 多维度校验确保质量
✅ **知识增强**: 知识库+搜索提升创作质量
✅ **灵活可扩展**: 易于添加新的 Agent 和工具
✅ **版本管理**: 支持剧本版本追踪和回溯

## 🔄 后续优化方向

- [ ] 集成 CrewAI 实现更智能的 Agent 协作
- [ ] 增强伏笔时序数据库（InfluxDB）
- [ ] 对接 Git 实现版本管理
- [ ] 支持本地大模型（Ollama + Llama 3）
- [ ] 增加更多剧本格式模板
- [ ] Web UI 界面

## 📄 许可证

本项目仅供学习和研究使用。

---

**Agent 搭建专家** | 多智能体编剧系统 v1.0
