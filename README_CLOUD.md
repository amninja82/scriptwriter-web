# 多智能体编剧系统 - 云端版

🎭 7个专业编剧智能体协作，为您打造精品剧本

## ✨ 特性

- ✅ **云端部署**：部署一次，随处访问
- ✅ **Token 持久化**：输入一次，永久使用
- ✅ **多设备支持**：手机、电脑都能用
- ✅ **对话历史**：自动保存到云端
- ✅ **无需安装**：打开网页就能用
- ✅ **免费部署**：使用 Vercel/Railway 等免费平台

## 🚀 快速开始

### 方式 1：使用部署脚本（推荐）

```bash
python deploy.py
```

按提示选择部署到 Vercel（免费）

### 方式 2：手动部署

查看 [CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md) 获取详细部署指南

## 📱 使用方法

1. **访问链接**：打开部署后的链接
2. **设置 Token**：
   - 点击左侧 "⚙️ Token 设置"
   - 输入您的 Coze API Token（在 https://coze.com/user/pat 获取）
3. **开始使用**：Token 保存后即可正常使用

## 🛠️ 技术栈

- **后端**：Flask (Python)
- **前端**：HTML + CSS + JavaScript
- **部署平台**：Vercel / Railway / Render

## 📁 项目结构

```
.
├── app.py                         # Flask 后端
├── scriptwriter_cloud.html        # 主页面
├── scriptwriter_settings.html     # 设置页面
├── requirements.txt               # Python 依赖
├── deploy.py                      # 部署脚本
├── CLOUD_DEPLOYMENT_GUIDE.md      # 部署指南
└── data/                          # 数据目录（自动创建）
    ├── tokens.json                # Token 存储
    └── chats.json                 # 对话历史
```

## 🔧 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务
python app.py

# 访问 http://localhost:5000
```

## 🌐 部署平台

| 平台 | 价格 | 难度 | 推荐度 |
|------|------|------|--------|
| Vercel | 免费 | ⭐ | ⭐⭐⭐⭐⭐ |
| Railway | 免费额度 | ⭐⭐ | ⭐⭐⭐⭐ |
| Render | 免费 | ⭐⭐ | ⭐⭐⭐⭐ |
| PythonAnywhere | 免费额度 | ⭐⭐⭐ | ⭐⭐⭐ |

## 🔒 安全说明

- Token 保存在云端服务器，不会泄露给第三方
- 建议使用 HTTPS（Vercel/Railway 等平台自动提供）
- 请妥善保管您的 Token

## 📖 功能说明

### 主页面功能

- 📝 对话聊天
- 📊 进度显示
- 🗑️ 清空历史
- ⚙️ Token 设置
- 💡 快捷操作

### 设置页面功能

- 🔑 输入/更新 Token
- ✅ Token 状态检查
- 💡 格式验证
- 🔒 云端持久化

## 🆘 常见问题

### Q: 部署后无法访问？

检查部署日志，确保依赖包正确安装。

### Q: Token 提示无效？

确认 Token 格式（以 pat_ 开头），检查是否过期。

### Q: 对话历史丢失？

确保 data/ 目录有写权限。

## 📄 许可证

MIT License

## 💬 技术支持

如有问题，请查看 [CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md)

---

**祝您创作愉快！** 🎬
