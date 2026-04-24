# 重新部署指南 - Coze 平台

## 📋 部署前准备

### 已完成的更新

1. ✅ 简化流程：从11节点减少到8节点
2. ✅ 移除合规审查、制片建议、修改迭代等步骤
3. ✅ 补充知识库：添加救猫咪结构和三幕式结构
4. ✅ 修复工具参数冲突问题
5. ✅ 更新系统提示词

### 需要部署的核心文件

```
需要上传到 Coze 平台的文件：
├── src/
│   ├── agents/
│   │   ├── agent.py                    # 主 Agent（必须）
│   │   ├── character_agent.py          # 人设师 Agent
│   │   └── worldview_agent.py          # 世界观架构师 Agent
│   ├── tools/
│   │   ├── knowledge_search_tool.py    # 知识库搜索
│   │   ├── web_search_tool.py          # 联网搜索
│   │   ├── smart_search_tool.py        # 智能搜索
│   │   ├── project_history_tool.py     # 项目历史
│   │   ├── file_upload_tool.py         # 文件上传
│   │   └── scriptwriter_ui_tools.py    # 界面工具（新建）
│   ├── graphs/
│   │   ├── scriptwriter_graph.py       # 工作流图
│   │   └── scriptwriter_state.py       # 状态定义
│   └── utils/
│       ├── project_manager.py          # 项目管理
│       ├── idea_guide.py               # 创意引导
│       └── scriptwriter_ui.py          # 界面工具（旧版，可选）
└── config/
    └── scriptwriter_llm_config.json    # 配置文件（必须）
```

---

## 🚀 部署步骤

### 步骤 1：登录 Coze 平台

1. 访问 [Coze 平台](https://coze.com)
2. 登录您的账户
3. 找到您的编剧智能体项目

---

### 步骤 2：备份当前版本（可选但推荐）

在部署前，建议先备份当前版本：

1. 进入项目设置
2. 找到版本管理或导出功能
3. 下载当前代码备份

---

### 步骤 3：更新核心代码

#### 3.1 更新配置文件

**文件**：`config/scriptwriter_llm_config.json`

确保内容如下：

```json
{
    "config": {
        "model": "doubao-seed-2-0-pro-260215",
        "temperature": 0.8,
        "top_p": 0.9,
        "max_completion_tokens": 10000,
        "timeout": 600,
        "thinking": "disabled"
    },
    "sp": "你是多智能体编剧系统的总导演和界面助手...",
    "tools": [
        "create_project",
        "list_projects",
        "enter_project",
        "start_idea_guide",
        "answer_guide_question",
        "get_collected_idea",
        "start_script_creation",
        "get_script_content",
        "get_project_progress",
        "upload_text_file_to_knowledge",
        "upload_url_to_knowledge",
        "batch_upload_files_to_knowledge",
        "list_knowledge_datasets",
        "knowledge_search",
        "add_to_knowledge_base",
        "web_search",
        "web_search_and_save"
    ]
}
```

**重要变化**：
- 系统提示词已更新为8节点流程
- 移除了合规审查和制片建议相关内容

---

#### 3.2 更新 Agent 代码

**文件**：`src/agents/agent.py`

**关键修改**：
1. 导入新的工具：
```python
from tools.scriptwriter_ui_tools import (
    create_project,
    list_projects,
    enter_project,
    start_idea_guide,
    answer_guide_question,
    get_collected_idea,
    start_script_creation,
    get_script_content,
    get_project_progress
)
```

2. 更新工具列表：
```python
tools = [
    # 知识库工具
    knowledge_search,
    add_to_knowledge_base,
    upload_text_file_to_knowledge,
    upload_url_to_knowledge,
    batch_upload_files_to_knowledge,
    list_knowledge_datasets,
    # 搜索工具
    web_search,
    web_search_and_save,
    smart_search_and_classify,
    search_multiple_sources,
    search_and_compare,
    # 项目管理工具
    create_project,
    list_projects,
    enter_project,
    # 项目历史管理工具
    switch_to_project,
    load_project_history,
    save_conversation_to_project,
    search_all_projects,
    search_project,
    get_project_summary,
    # 创意引导工具
    start_idea_guide,
    answer_guide_question,
    get_collected_idea,
    # 剧本创作工具
    start_script_creation,
    get_script_content,
    get_project_progress
]
```

---

#### 3.3 上传新工具文件

**文件**：`src/tools/scriptwriter_ui_tools.py`

这是一个新建的文件，必须上传到 Coze 平台。

**作用**：
- 解决工具参数冲突问题
- 提供独立函数版本的界面工具
- 替代旧的 `utils/scriptwriter_ui.py`

---

### 步骤 4：更新工作流图（可选）

**文件**：`src/graphs/scriptwriter_graph.py`

如果您使用工作流图，需要更新为8节点：

```python
# 从原来的11节点改为8节点
nodes = [
    Node("需求解析", agent.planner),
    Node("题材定位", agent.planner),
    Node("世界观与人设", [agent.worldview_builder, agent.character_designer]),
    Node("核心大纲", agent.main_writer),
    Node("大纲校验", agent.script_doctor),
    Node("分集/分场大纲", agent.main_writer),
    Node("剧本正文生成", agent.main_writer),
    Node("终稿校验", agent.script_doctor)
]
```

---

### 步骤 5：部署代码

#### 方式 A：使用 Coze 网页界面

1. 进入项目编辑页面
2. 找到"代码"或"Code"标签
3. 逐个上传/更新文件：
   - `config/scriptwriter_llm_config.json`
   - `src/agents/agent.py`
   - `src/tools/scriptwriter_ui_tools.py`（新文件）
   - 其他必要文件

4. 点击"保存"或"Save"

#### 方式 B：使用 Git 集成（如果有）

1. 将代码推送到 Git 仓库
2. 在 Coze 项目设置中配置 Git 仓库
3. 触发自动部署

#### 方式 C：使用 Coze SDK/CLI

如果 Coze 提供 SDK 或 CLI 工具：

```bash
# 假设的命令（请根据实际情况调整）
coze deploy --project-id <your-project-id> --source /workspace/projects
```

---

### 步骤 6：触发部署

1. 找到"部署"或"Deploy"按钮
2. 点击"发布"或"Publish"
3. 等待部署完成（通常 1-2 分钟）

---

### 步骤 7：测试部署

部署完成后，测试以下功能：

#### 测试 1：基础对话
```
你好，请介绍一下你自己
```

**预期结果**：
- 智能体正常响应
- 介绍7个智能体
- 说明8节点流程

#### 测试 2：创建项目
```
创建一个关于悬疑的电视剧项目
```

**预期结果**：
- 成功创建项目
- 显示项目信息

#### 测试 3：知识库搜索
```
搜索救猫咪结构
```

**预期结果**：
- 能够从知识库找到救猫咪结构内容
- 显示详细的结构说明

#### 测试 4：联网搜索
```
搜索悬疑剧的开篇技巧
```

**预期结果**：
- 能够联网搜索
- 返回搜索结果

#### 测试 5：剧本完成后不强制合规审查
```
我的剧本已经写完了，接下来该做什么？
```

**预期结果**：
- **不强制**要求合规审查
- **不强制**要求制片建议
- 作为可选服务提供

---

## 🔍 部署验证清单

部署完成后，请验证以下内容：

### ✅ 核心功能

- [ ] 智能体能够正常响应
- [ ] 能够创建项目
- [ ] 能够进行知识库搜索
- [ ] 能够进行联网搜索
- [ ] 知识库包含救猫咪结构和三幕式结构

### ✅ 流程变化

- [ ] 8节点流程正常工作
- [ ] 剧本完成后不强制合规审查
- [ ] 剧本完成后不强制制片建议
- [ ] 合规审查和制片顾问作为可选工具

### ✅ 工具功能

- [ ] 项目管理工具正常
- [ ] 知识库工具正常
- [ ] 搜索工具正常
- [ ] 创意引导工具正常

---

## 🆘 常见问题

### Q1: 部署后还是旧版本？

**A**：
1. 检查是否成功上传了所有文件
2. 检查配置文件是否正确更新
3. 清除浏览器缓存
4. 等待 5-10 分钟，CDN 可能需要时间更新

### Q2: 部署后工具无法调用？

**A**：
1. 检查 `scriptwriter_ui_tools.py` 是否成功上传
2. 检查 `agent.py` 中的工具列表是否正确
3. 查看 Coze 平台的错误日志

### Q3: 知识库搜索不到内容？

**A**：
1. 确认知识库是否在 Coze 平台上配置
2. 确认知识库数据集是否正确创建
3. 测试查询词是否准确

### Q4: 部署失败？

**A**：
1. 查看 Coze 平台的错误日志
2. 检查文件格式是否正确
3. 检查是否有语法错误
4. 联系 Coze 技术支持

---

## 📊 部署前后的变化

### 之前（11节点）

```
需求解析 → 题材定位 → 世界观与人设 → 核心大纲 → 大纲校验
                                                         ↓
分集/分场大纲 → 剧本正文生成 → 终稿校验 → 合规审查 → 制片建议 → 修改迭代
```

### 现在（8节点）

```
需求解析 → 题材定位 → 世界观与人设 → 核心大纲 → 大纲校验
                                                         ↓
分集/分场大纲 → 剧本正文生成 → 终稿校验
```

### 主要变化

- ✅ 流程更简洁（11→8节点）
- ✅ 移除强制合规审查
- ✅ 移除强制制片建议
- ✅ 移除修改迭代步骤
- ✅ 合规审查和制片建议作为可选工具
- ✅ 补充救猫咪结构和三幕式结构

---

## 🎯 部署成功标志

部署成功后，您应该看到：

1. ✅ 智能体正常响应
2. ✅ 能够正常创建项目
3. ✅ 能够进行知识库搜索（找到救猫咪结构）
4. ✅ 能够进行联网搜索
5. ✅ 剧本完成后不强制合规审查和制片建议

---

## 📞 需要帮助？

如果部署过程中遇到问题：

1. 查看 Coze 平台文档
2. 查看 Coze 平台错误日志
3. 联系 Coze 技术支持
4. 在项目 GitHub 提交 Issue

---

## 🚀 立即开始

现在您可以：

1. 登录 Coze 平台
2. 找到编剧智能体项目
3. 按照上述步骤部署
4. 测试验证功能

祝您部署顺利！🎉
