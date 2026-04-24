# Vercel 部署指南 - 网页版

## 🚀 快速部署到 Vercel（推荐）

### 前置条件
- ✅ 已注册 Vercel 账户
- ✅ 有一个 Git 仓库（GitHub / GitLab / Bitbucket）

---

## 📋 部署步骤

### 方式 1：使用 Vercel CLI（推荐）

#### 步骤 1：安装 Vercel CLI

```bash
# 如果是 Windows，打开 PowerShell 或 CMD
npm install -g vercel
```

#### 步骤 2：登录 Vercel

```bash
vercel login
```

按提示操作：
1. 选择登录方式（GitHub / GitLab / Email）
2. 完成登录验证

#### 步骤 3：进入项目目录

```bash
cd /workspace/projects
```

#### 步骤 4：初始化 Git 仓库（如果还没有）

```bash
git init
git add .
git commit -m "初始化编剧智能体网页版"
```

#### 步骤 5：推送到 GitHub

```bash
# 1. 在 GitHub 创建新仓库
# 2. 添加远程仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

#### 步骤 6：部署到 Vercel

```bash
vercel
```

按提示操作：
```
? Set up and deploy "~/workspace/projects"? [Y/n] → 输入 Y
? Which scope do you want to deploy to? → 选择你的账户
? Link to existing project? [y/N] → 输入 N
? What's your project's name? → 输入 scriptwriter-web
? In which directory is your code located? → 直接回车（使用当前目录）
? Want to modify these settings? [y/N] → 输入 N
```

等待部署完成，Vercel 会给您一个访问链接，例如：
```
https://scriptwriter-web.vercel.app
```

#### 步骤 7：正式部署

```bash
vercel --prod
```

---

### 方式 2：使用 Vercel 网页界面（简单）

#### 步骤 1：推送代码到 GitHub

```bash
cd /workspace/projects
git init
git add .
git commit -m "初始化编剧智能体网页版"
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

#### 步骤 2：登录 Vercel 网页

1. 访问 [Vercel](https://vercel.com)
2. 登录您的账户

#### 步骤 3：创建新项目

1. 点击 **"Add New"** 或 **"New Project"**
2. 选择您的 GitHub 仓库
3. 点击 **"Import"**

#### 步骤 4：配置项目

**Framework Preset**: 选择 **"Python"**

**Build Command**:
```
pip install -r requirements.txt && python app.py
```

**Output Directory**: 留空

**Install Command**:
```
pip install -r requirements.txt
```

#### 步骤 5：环境变量（可选）

如果需要配置环境变量：
1. 在项目设置中找到 **"Environment Variables"**
2. 添加需要的环境变量

#### 步骤 6：部署

点击 **"Deploy"** 按钮，等待部署完成。

---

## 📁 需要的文件清单

确保您的项目包含以下文件：

```
workspace/projects/
├── app.py                         # Flask 后端 ✅ 必须
├── requirements.txt               # Python 依赖 ✅ 必须
├── scriptwriter_cloud.html        # 主页面 ✅ 必须
├── scriptwriter_settings.html     # 设置页面 ✅ 必须
├── vercel.json                    # Vercel 配置 ✅ 推荐
└── data/                          # 数据目录（自动创建）
    ├── tokens.json
    └── chats.json
```

---

## 🔧 Vercel 配置文件（vercel.json）

如果还没有，创建 `vercel.json`：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/app.py"
    }
  ],
  "env": {
    "PORT": "5000"
  }
}
```

---

## ⚙️ Requirements.txt

确保 `requirements.txt` 包含：

```
Flask==3.0.0
requests==2.31.0
```

---

## 🧪 测试部署

部署完成后，测试以下功能：

### 测试 1：访问主页

打开访问链接，例如：
```
https://scriptwriter-web.vercel.app
```

**预期**：
- 显示编剧智能体界面
- 左侧有项目列表
- 右侧有聊天区域

### 测试 2：设置 Token

1. 点击左侧 **"⚙️ Token 设置"** 按钮
2. 输入 Coze API Token
3. 点击 **"保存 Token"**

**预期**：
- Token 保存成功
- 状态显示"已设置 Token"
- 可以开始使用

### 测试 3：创建项目

1. 输入消息："创建一个测试项目"
2. 点击发送

**预期**：
- 成功创建项目
- 显示项目信息

### 测试 4：联网搜索

1. 点击左侧 **"🔍 联网搜索"** 按钮
2. 输入搜索内容
3. 点击搜索

**预期**：
- 成功搜索
- 返回搜索结果

---

## 🆘 常见问题

### Q1: 部署后 404 错误？

**A**：
1. 检查 `vercel.json` 配置是否正确
2. 检查 `app.py` 是否在根目录
3. 查看部署日志

### Q2: 部署失败，提示 Python 错误？

**A**：
1. 检查 `requirements.txt` 是否正确
2. 检查 Python 版本（建议 3.9+）
3. 查看详细错误日志

### Q3: 无法访问 API？

**A**：
1. 检查 API 地址是否正确
2. 检查 Token 是否有效
3. 检查网络连接

### Q4: Token 无法保存？

**A**：
1. 检查 `data/` 目录权限
2. 查看 Vercel 存储配置
3. 确认环境变量设置

---

## 📊 部署状态检查

### 查看部署日志

1. 登录 Vercel 网页
2. 进入项目页面
3. 点击 **"Deployments"**
4. 点击最新的部署记录
5. 查看详细日志

### 查看实时日志

```bash
vercel logs
```

---

## 🎯 自定义域名（可选）

### 添加自定义域名

1. 进入项目设置
2. 点击 **"Domains"**
3. 添加您的域名
4. 按提示配置 DNS

---

## 🔄 更新部署

### 更新代码后重新部署

```bash
# 1. 提交代码
git add .
git commit -m "更新功能"
git push

# 2. Vercel 会自动部署
# 或手动触发
vercel --prod
```

---

## 💡 最佳实践

### 1. 使用环境变量

敏感信息（如 API 密钥）应该使用环境变量：

```python
import os

API_KEY = os.getenv("COZE_API_KEY")
```

在 Vercel 项目设置中添加环境变量。

### 2. 错误处理

添加适当的错误处理：

```python
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': str(error)}), 500
```

### 3. 日志记录

添加日志记录：

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logger.info("访问主页")
    return send_from_directory('.', 'scriptwriter_cloud.html')
```

---

## 🎉 部署成功！

部署成功后，您会得到：

✅ 一个访问链接，例如：`https://scriptwriter-web.vercel.app`
✅ 可以通过网址访问
✅ 支持多设备使用
✅ Token 云端保存
✅ 对话历史云端同步

---

## 📞 需要帮助？

如果部署过程中遇到问题：

1. 查看 Vercel 文档
2. 查看部署日志
3. 联系 Vercel 支持
4. 在 GitHub 提交 Issue

祝您部署顺利！🚀
