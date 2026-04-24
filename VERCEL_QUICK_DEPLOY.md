# 🚀 Vercel 部署快速指南

## ⚡ 一键部署（推荐）

### 前提条件
- ✅ 已注册 [Vercel](https://vercel.com) 账户
- ✅ 已注册 [GitHub](https://github.com) 账户
- ✅ 已安装 Git
- ✅ 已安装 Node.js（用于安装 Vercel CLI）

### 步骤 1：安装 Vercel CLI

```bash
npm install -g vercel
```

### 步骤 2：登录 Vercel

```bash
vercel login
```

按提示操作完成登录。

### 步骤 3：推送到 GitHub

```bash
# 1. 在 GitHub 创建新仓库
# 2. 初始化 Git 仓库（如果还没有）
git init

# 3. 添加所有文件
git add .

# 4. 提交代码
git commit -m "初始化编剧智能体网页版"

# 5. 添加远程仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 6. 设置主分支
git branch -M main

# 7. 推送到 GitHub
git push -u origin main
```

### 步骤 4：部署到 Vercel

```bash
# 进入项目目录
cd /workspace/projects

# 部署（预览版）
vercel

# 部署（正式版）
vercel --prod
```

按提示操作：
- 选择账户
- 选择项目（如果没有，创建新项目）
- 项目名称：`scriptwriter-web`
- 目录：当前目录
- 使用默认配置

### 步骤 5：访问网页版

部署完成后，Vercel 会给您一个访问链接，例如：
```
https://scriptwriter-web.vercel.app
```

打开链接即可使用！

---

## 📋 或者使用自动部署脚本

```bash
python deploy_to_vercel.py
```

脚本会自动完成所有步骤！

---

## 🔧 需要的文件

确保您的项目包含以下文件：

```
workspace/projects/
├── app.py                         # Flask 后端 ✅
├── requirements.txt               # Python 依赖 ✅
├── vercel.json                    # Vercel 配置 ✅
├── scriptwriter_cloud.html        # 主页面 ✅
├── scriptwriter_settings.html     # 设置页面 ✅
└── deploy_to_vercel.py            # 部署脚本 ✅
```

---

## ⚙️ 配置 Coze API Token

### 1. 获取 Coze API Token

- 访问 [Coze 平台](https://www.coze.cn)
- 登录您的账户
- 进入 API 设置页面
- 复制您的 API Token

### 2. 在网页版中配置

1. 打开部署后的网页版链接
2. 点击左侧 **"⚙️ Token 设置"** 按钮
3. 输入您的 Coze API Token
4. 点击 **"保存 Token"**
5. 完成！

---

## 🧪 测试功能

### 测试 1：创建项目

输入消息："创建一个测试项目"

**预期**：成功创建项目，显示项目信息

### 测试 2：联网搜索

1. 点击左侧 **"🔍 联网搜索"** 按钮
2. 输入搜索内容
3. 点击搜索

**预期**：成功搜索，返回搜索结果

---

## 🔄 更新部署

### 修改代码后重新部署

```bash
# 1. 提交更改
git add .
git commit -m "更新功能"
git push

# 2. Vercel 会自动部署
# 或手动触发
vercel --prod
```

---

## 🆘 常见问题

### Q1: 部署后 404 错误？

**A**：
1. 检查 `vercel.json` 配置是否正确
2. 检查 `app.py` 是否在根目录
3. 查看部署日志

### Q2: Token 无法保存？

**A**：
1. Vercel 的免费版存储有限，可能不持久化
2. 推荐使用环境变量配置 Token
3. 或升级 Vercel 计划

### Q3: API 调用失败？

**A**：
1. 检查 Token 是否有效
2. 检查 API 地址是否正确
3. 查看 Vercel 部署日志

---

## 💡 最佳实践

### 使用环境变量配置 Token

在 Vercel 项目设置中添加环境变量：

1. 进入项目设置
2. 点击 **"Environment Variables"**
3. 添加：
   - Name: `COZE_API_TOKEN`
   - Value: `你的 API Token`

然后在代码中使用：

```python
import os

API_TOKEN = os.getenv("COZE_API_TOKEN", "")
```

---

## 📞 需要帮助？

- 查看 [Vercel 文档](https://vercel.com/docs)
- 查看 [Vercel Python 部署指南](https://vercel.com/docs/concepts/solutions/serverless-functions/runtimes/python)
- 在 GitHub 提交 Issue

---

## 🎉 完成后

部署成功后，您会得到：

✅ 一个访问链接，例如：`https://scriptwriter-web.vercel.app`
✅ 可以通过网址访问
✅ 支持多设备使用
✅ Token 云端保存
✅ 对话历史云端同步

祝您使用愉快！🚀
