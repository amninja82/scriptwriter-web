# 🚀 部署到 Vercel - 三种方法

## 方法 1：Vercel Git 集成（最简单）⭐ 推荐

这是最简单的方法，通过 Vercel 的 Git 集成自动部署！

### 步骤 1：访问 Vercel

打开 https://vercel.com，您应该已经登录了。

### 步骤 2：创建新项目

1. 点击 **"Add New"** 或 **"New Project"**
2. 点击 **"Continue with GitHub"**
3. 授权 Vercel 访问您的 GitHub 仓库
4. 选择 **amninja82/scriptwriter-web** 仓库
5. 点击 **"Import"**

### 步骤 3：配置项目

**Framework Preset**: 选择 **"Other"** 或 **"Python"**

**Build and Output Settings**:
- **Build Command**: 留空
- **Output Directory**: 留空
- **Install Command**: 留空

**Environment Variables** (可选):
- 不需要添加任何环境变量

### 步骤 4：部署

点击 **"Deploy"** 按钮！

等待 1-2 分钟，部署完成后会显示一个访问链接，例如：
```
https://scriptwriter-web.vercel.app
```

### 完成！

打开链接即可使用！

---

## 方法 2：使用本地 Vercel CLI

如果您已经在本地登录了 Vercel：

### 步骤 1：克隆代码到本地

```bash
# 在您的电脑上运行
cd Desktop
mkdir scriptwriter-web
cd scriptwriter-web
git clone https://github.com/amninja82/scriptwriter-web.git .
```

### 步骤 2：部署

```bash
vercel
vercel --prod
```

---

## 方法 3：使用 GitHub Actions（已配置）

GitHub Actions 已配置，但需要设置 Secrets。

### 需要的 Secrets：

1. **VERCEL_TOKEN**
2. **VERCEL_ORG_ID**
3. **VERCEL_PROJECT_ID**

### 获取这些值：

#### 1. 获取 VERCEL_TOKEN

1. 访问 https://vercel.com/account/tokens
2. 点击 **"Create Token"**
3. 输入名称（例如 "GitHub Actions"）
4. 复制 Token

#### 2. 获取 VERCEL_ORG_ID 和 VERCEL_PROJECT_ID

1. 在 Vercel 中创建项目（方法 1）
2. 进入项目设置
3. 查看 General Settings
4. 复制 Project ID

Organization ID 通常在 Vercel 设置页面的团队信息中。

#### 3. 配置 GitHub Secrets

1. 访问 https://github.com/amninja82/scriptwriter-web/settings/secrets/actions
2. 点击 **"New repository secret"**
3. 添加三个 secrets：
   - Name: `VERCEL_TOKEN`, Value: 您的 Vercel Token
   - Name: `VERCEL_ORG_ID`, Value: 您的 Organization ID
   - Name: `VERCEL_PROJECT_ID`, Value: 您的 Project ID

#### 4. 触发部署

1. 访问 https://github.com/amninja82/scriptwriter-web/actions
2. 点击 **"Deploy to Vercel"** workflow
3. 点击 **"Run workflow"**

---

## ✅ 推荐：使用方法 1

**最简单、最快速！**

只需要在 Vercel 网页上导入 GitHub 仓库，点击部署即可！

---

## 🎯 快速开始（方法 1）

1. 打开 https://vercel.com
2. 点击 **"Add New"** → **"Project"**
3. 选择 **scriptwriter-web** 仓库
4. 点击 **"Deploy"**
5. 完成！

---

## 📱 部署后配置

### 配置 Coze API Token

1. 打开 Vercel 给您的访问链接
2. 点击 **"⚙️ Token 设置"**
3. 输入 Coze API Token
4. 开始使用！

---

## 💡 选择哪种方法？

| 方法 | 难度 | 优点 | 推荐度 |
|------|------|------|--------|
| 方法 1 (Git 集成) | ⭐ 最简单 | 自动部署，无需配置 | ⭐⭐⭐⭐⭐ |
| 方法 2 (本地 CLI) | ⭐⭐ 简单 | 需要克隆代码 | ⭐⭐⭐ |
| 方法 3 (GitHub Actions) | ⭐⭐⭐⭐ 复杂 | 需要配置 Secrets | ⭐⭐ |

**强烈推荐方法 1！** 🚀
