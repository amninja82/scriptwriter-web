# 快速部署清单

## ⚡ 快速部署步骤（5分钟）

### 1️⃣ 必须更新的文件（3个）

| 文件 | 状态 | 说明 |
|------|------|------|
| `config/scriptwriter_llm_config.json` | ✅ 必须更新 | 8节点流程配置 |
| `src/agents/agent.py` | ✅ 必须更新 | 主Agent代码 |
| `src/tools/scriptwriter_ui_tools.py` | ✅ 必须上传 | 新建的界面工具 |

### 2️⃣ 可选更新的文件

| 文件 | 说明 |
|------|------|
| `src/graphs/scriptwriter_graph.py` | 如果使用工作流图，需要更新为8节点 |
| `src/tools/smart_search_tool.py` | 如果之前有修改，建议同步 |

---

## 📝 部署步骤

### 步骤 1：登录 Coze 平台
- 访问 https://coze.com
- 登录账户
- 找到编剧智能体项目

### 步骤 2：更新配置文件
- 打开 `config/scriptwriter_llm_config.json`
- 确认内容为8节点流程
- 上传到 Coze 平台

### 步骤 3：更新 Agent 代码
- 打开 `src/agents/agent.py`
- 确认导入新工具
- 上传到 Coze 平台

### 步骤 4：上传新工具
- 找到 `src/tools/scriptwriter_ui_tools.py`
- 上传到 Coze 平台

### 步骤 5：触发部署
- 点击"部署"或"发布"
- 等待 1-2 分钟

### 步骤 6：测试功能
- 测试基础对话
- 测试创建项目
- 测试知识库搜索
- 测试剧本完成后的提示

---

## ✅ 验证清单

部署完成后，验证：

- [ ] 智能体正常响应
- [ ] 能够创建项目
- [ ] 能够搜索救猫咪结构
- [ ] 能够联网搜索
- [ ] 剧本完成后不强制合规审查

---

## 🆘 如果失败

1. 查看 Coze 错误日志
2. 检查文件是否全部上传
3. 确认配置文件正确
4. 尝试重新部署

详细部署指南请查看 [REDEPLOYMENT_GUIDE.md](REDEPLOYMENT_GUIDE.md)
