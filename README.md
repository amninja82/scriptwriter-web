# 多智能体编剧系统

🎭 7个专业编剧智能体协作，为您打造精品剧本

## ✨ 系统特性

- ✅ **7个专业智能体**：策划师、世界观架构师、人设师、主笔编剧、剧本医生、合规专员、制片顾问
- ✅ **8节点创作流程**：从需求到终稿的完整创作流水线
- ✅ **知识库集成**：内置专业编剧知识库，支持联网搜索并自动分类保存
- ✅ **项目管理**：创建多个项目，独立管理对话历史
- ✅ **版本多样**：图形界面版、命令行版、云端版
- ✅ **本地存储**：对话历史保存在本地，数据安全

## 🚀 快速开始

### 方式 1：GUI 版本（推荐）⭐⭐⭐⭐⭐

```bash
# 直接运行
python scriptwriter_gui.py

# 或打包为 exe
build_windows_gui.bat
```

**特点**：
- 图形界面，操作简单
- 项目管理，对话历史本地存储
- 联网搜索，自动保存到知识库
- 支持导出对话记录

详细教程：[GUI 版本使用指南](GUI_VERSION_GUIDE.md)

---

### 方式 2：命令行版本（次推荐）⭐⭐⭐⭐

```bash
# 使用终极修复版（推荐）
python scriptwriter_cli_final.py

# 或打包为 exe
build_windows.bat
```

**特点**：
- 命令行操作
- 实时进度显示
- 5 分钟超时
- 增强错误处理

详细教程：[exe 修复指南](EXE_FIX_GUIDE.md)

---

### 方式 3：Coze API 版本（需要重新部署）⚠️

**地址**：https://2km4yszdhf.coze.site/stream_run

**当前状态**：
- 代码已更新，需要重新部署到 Coze 平台

**部署方式**：
1. 登录 Coze 平台
2. 上传最新代码
3. 重新部署
4. 获取访问链接

详细教程：[云端部署指南](CLOUD_DEPLOYMENT_GUIDE.md)

---

## 📊 版本对比

| 版本 | 图形界面 | 项目管理 | 对话历史 | 本地运行 | 推荐度 |
|------|----------|----------|----------|----------|--------|
| **GUI 版本** | ✅ | ✅ | ✅ 本地 | ✅ | ⭐⭐⭐⭐⭐ |
| **CLI 版本** | ❌ | ❌ | ❌ | ✅ | ⭐⭐⭐⭐ |
| **Coze API 版本** | ✅ | ✅ | ✅ 云端 | ❌ | ⭐⭐⭐ |

详细对比：[版本对比与选择指南](VERSION_COMPARISON.md)

---

## 🎯 核心功能

### 1. 7个专业智能体

1. **策划师 Agent** - 需求解析、题材定位、受众分析
2. **世界观架构师 Agent** - 世界观设定构建
3. **人设师 Agent** - 人物档案创建
4. **主笔编剧 Agent** - 大纲创作、剧本正文生成
5. **剧本医生 Agent** - 质量审查、修改建议
6. **合规专员 Agent** - 合规性检查（可选）
7. **制片顾问 Agent** - 商业价值评估（可选）

### 2. 8节点创作流程

```
需求解析 → 题材定位 → 世界观与人设 → 核心大纲 → 大纲校验
                                                         ↓
分集/分场大纲 → 剧本正文生成 → 终稿校验
```

详细说明：[工作流程指南](WORKFLOW_GUIDE.md)

### 3. 知识库系统

#### Coze 平台知识库（云端）
- 编剧技巧
- 题材分析
- 故事钩子
- 情绪价值
- 冲突设计
- 影视案例

#### 联网搜索 + 自动保存
- 联网搜索最新内容
- AI 自动分析类型
- 自动分类保存到知识库

### 4. 项目管理

- 创建多个项目
- 切换项目自动加载历史
- 对话历史本地存储
- 导出对话记录

---

## 💡 使用示例

### 示例 1：创建电视剧项目

```
你：创建一个关于时间旅行的科幻电视剧项目

智能体：✅ 项目创建成功！

项目信息：
- 项目名称：《时空交错》
- 项目类型：电视剧
- 创建时间：2024-01-01

接下来可以：
1. 输入创意完善细节
2. 启动创意引导
3. 开始创作剧本
```

### 示例 2：创意引导

```
你：启动创意引导

智能体：🎬 欢迎使用多智能体编剧系统！

请告诉我你的创作创意，可以是一句话、一个想法或一个场景。

例如：
- "我想写一个古代宫廷悬疑剧"
- "关于未来世界的爱情故事"
- "一个侦探破案的悬疑剧"

请开始描述你的创意 👇
```

### 示例 3：联网搜索

```
你：搜索悬疑剧的开篇技巧并保存到知识库

智能体：🔍 正在搜索：悬疑剧开篇技巧...

✅ 搜索完成！

已为您找到以下内容：
1. 悬疑剧开篇的3种常见模式...
2. 经典案例分析...
3. 创作建议...

已自动分类保存到知识库，下次可以直接使用！
```

---

## 📁 项目结构

```
.
├── scriptwriter_gui.py           # GUI 版本主程序 ⭐推荐
├── scriptwriter_cli_final.py     # CLI 版本（终极修复版）
├── scriptwriter_cli_windows.py   # CLI 版本（Windows 兼容版）
├── scriptwriter_cli_sse.py       # CLI 版本（SSE 修复版）
│
├── build_windows.bat             # CLI 版本打包脚本
├── build_windows_gui.bat         # GUI 版本打包脚本
│
├── src/                          # 源代码目录
│   ├── agents/                   # Agent 代码
│   │   ├── agent.py              # 主 Agent
│   │   ├── character_agent.py    # 人设师 Agent
│   │   └── worldview_agent.py    # 世界观架构师 Agent
│   ├── tools/                    # 工具代码
│   │   ├── knowledge_search_tool.py
│   │   ├── web_search_tool.py
│   │   ├── smart_search_tool.py
│   │   ├── project_history_tool.py
│   │   └── scriptwriter_ui_tools.py
│   ├── graphs/                   # 工作流代码
│   │   ├── scriptwriter_graph.py
│   │   └── scriptwriter_state.py
│   └── utils/                    # 工具代码
│       ├── project_manager.py
│       ├── idea_guide.py
│       └── scriptwriter_ui.py
│
├── config/                       # 配置文件
│   └── scriptwriter_llm_config.json
│
├── docs/                         # 文档目录
│
├── GUI_VERSION_GUIDE.md          # GUI 版本使用指南
├── EXE_FIX_GUIDE.md              # exe 修复指南
├── CLOUD_DEPLOYMENT_GUIDE.md     # 云端部署指南
├── VERSION_COMPARISON.md         # 版本对比指南
├── WORKFLOW_GUIDE.md             # 工作流程指南
└── README.md                     # 本文件
```

---

## 🔧 技术栈

- **框架**：LangGraph 1.0 + LangChain
- **模型**：豆包 4.0 Ultra（doubao-seed-2-0-pro-260215）
- **知识库**：Coze 平台知识库
- **GUI**：tkinter
- **打包**：PyInstaller

---

## 📖 文档

| 文档 | 说明 |
|------|------|
| [GUI_VERSION_GUIDE.md](GUI_VERSION_GUIDE.md) | GUI 版本详细使用指南 |
| [EXE_FIX_GUIDE.md](EXE_FIX_GUIDE.md) | exe 版本修复指南 |
| [CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md) | 云端部署详细指南 |
| [VERSION_COMPARISON.md](VERSION_COMPARISON.md) | 版本对比与选择指南 |
| [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) | 8节点工作流程指南 |

---

## ⚠️ 重要提示

### 1. API Token 安全

- Token 保存在本地文件中
- 请妥善保管，不要泄露给他人
- 定期更换 Token

**获取 Token**：https://coze.com/user/pat

### 2. 网络连接

- 所有版本都需要网络连接才能使用
- 联网搜索需要稳定的网络环境
- 建议使用稳定的网络

### 3. 数据存储

- **GUI 版本**：对话历史保存在本地 `scriptwriter_gui_data.json`
- **CLI 版本**：对话历史保存在 Coze 平台
- **Coze API 版本**：对话历史保存在云端

### 4. 知识库

所有版本使用**相同的知识库**：
- Coze 平台知识库（云端）
- 联网搜索自动保存

---

## 🆘 常见问题

### Q1: 如何选择版本？

**A**：
- 日常创作：推荐 **GUI 版本**
- 快速测试：推荐 **CLI 版本**
- 团队协作：推荐 **Coze API 版本**（需要重新部署）

详细对比：[版本对比与选择指南](VERSION_COMPARISON.md)

### Q2: 知识库在哪里？

**A**：
知识库在 Coze 平台，所有版本共享同一个知识库：
- 位置：Coze 平台
- 内容：编剧技巧、题材分析、故事钩子等
- 访问：智能体自动调用

### Q3: 如何联网搜索并保存？

**A**：
- **GUI 版本**：点击 "🔍 联网搜索" 按钮
- **CLI 版本**：输入 "搜索XX并保存到知识库"
- **Coze API 版本**：直接对话

### Q4: 对话历史保存在哪里？

**A**：
- **GUI 版本**：本地 `scriptwriter_gui_data.json`
- **CLI 版本**：Coze 平台（云端）
- **Coze API 版本**：Coze 平台（云端）

### Q5: 如何重新部署云端版本？

**A**：
1. 登录 Coze 平台
2. 找到编剧智能体项目
3. 上传最新代码
4. 点击"部署"
5. 等待部署完成

详细教程：[云端部署指南](CLOUD_DEPLOYMENT_GUIDE.md)

---

## 🎯 快速选择

### 你想要：

**图形界面？**
→ [GUI 版本](scriptwriter_gui.py) ⭐推荐

**命令行？**
→ [CLI 版本](scriptwriter_cli_final.py)

**云端访问？**
→ Coze API 版本（需要重新部署）

**本地保存？**
→ [GUI 版本](scriptwriter_gui.py)

**快速测试？**
→ [CLI 版本](scriptwriter_cli_final.py)

**团队协作？**
→ Coze API 版本（需要重新部署）

---

## 📄 许可证

MIT License

---

## 💬 技术支持

如有问题，请：
1. 查看相关文档
2. 检查常见问题
3. 尝试重新运行

---

## 🎉 立即开始

```bash
# 1. 下载代码

# 2. 安装依赖
pip install requests

# 3. 运行程序
python scriptwriter_gui.py

# 4. 设置 Token
# 点击 "⚙️ 设置 Token" 按钮

# 5. 开始创作
# 创建项目，开始对话！
```

**祝您创作愉快！** 🎬
