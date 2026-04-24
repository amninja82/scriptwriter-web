# 云端部署指南 - 多智能体编剧系统

本文档介绍如何将编剧系统部署到云端，提供统一的访问链接。

## 📦 部署方式

### 方式 1：Vercel（推荐，免费）

#### 步骤 1：准备代码

确保您的项目包含以下文件：
- `app.py` - Flask 后端
- `scriptwriter_cloud.html` - 主页面
- `scriptwriter_settings.html` - 设置页面
- `requirements.txt` - 依赖包
- `data/` - 数据目录（会自动创建）

#### 步骤 2：安装 Vercel CLI

```bash
npm install -g vercel
```

#### 步骤 3：登录 Vercel

```bash
vercel login
```

#### 步骤 4：部署

在项目根目录执行：

```bash
vercel
```

按提示操作：
1. ? Set up and deploy "~/workspace/projects"? [Y/n] → 输入 Y
2. ? Which scope do you want to deploy to? → 选择您的账户
3. ? Link to existing project? [y/N] → 输入 N
4. ? What's your project's name? → 输入 scriptwriter-cloud
5. ? In which directory is your code located? → 直接回车（使用当前目录）
6. ? Want to modify these settings? [y/N] → 输入 N

等待部署完成，Vercel 会给您一个访问链接，例如：
```
https://scriptwriter-cloud.vercel.app
```

#### 步骤 5：配置 Python 环境

Vercel 默认使用 Node.js，需要配置 Python 环境：

1. 访问 Vercel 项目页面
2. 点击 Settings → Build & Development → Runtime
3. 将 Runtime 改为 "Python 3.9"

#### 步骤 6：添加 requirements.txt

确保 `requirements.txt` 在项目根目录。

---

### 方式 2：Railway（推荐，免费额度）

#### 步骤 1：安装 Railway CLI

```bash
npm install -g @railway/cli
```

#### 步骤 2：登录 Railway

```bash
railway login
```

#### 步骤 3：初始化项目

```bash
railway init
```

#### 步骤 4：配置环境

在项目目录创建 `railway.toml` 文件：

```toml
[build]
builder = "nixpacks"

[build.env]
NIXPACKS_PYTHON_VERSION = "3.9"

[build.settings]
run-on-build = "pip install -r requirements.txt"

[[services]]
name = "app"
env = "PORT"
env_default = "5000"

[[services.ports]]
number = 5000

[[services.ports]]
handlers = ["http"]
port = 5000
```

#### 步骤 5：部署

```bash
railway up
```

Railway 会自动部署，完成后给您一个访问链接。

---

### 方式 3：Render（免费）

#### 步骤 1：准备代码

在项目根目录创建 `render.yaml` 文件：

```yaml
services:
  - type: web
    name: scriptwriter-cloud
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: PORT
        value: 5000
```

#### 步骤 2：部署

1. 登录 [Render](https://render.com)
2. 点击 "New +" → "Web Service"
3. 连接您的 GitHub 仓库
4. 选择根目录
5. 选择 "Python 3" 运行时
6. 点击 "Create Web Service"

---

### 方式 4：Heroku（需要信用卡）

#### 步骤 1：安装 Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# 下载并安装 https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 步骤 2：登录 Heroku

```bash
heroku login
```

#### 步骤 3：创建应用

```bash
heroku create scriptwriter-cloud
```

#### 步骤 4：部署

```bash
git init
git add .
git commit -m "Initial commit"
git push heroku master
```

---

### 方式 5：自己的服务器（推荐）

如果您有自己的服务器（阿里云、腾讯云等），可以使用以下方式：

#### 使用 systemd（推荐）

1. 创建服务文件 `/etc/systemd/system/scriptwriter.service`：

```ini
[Unit]
Description=Scriptwriter Cloud Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/your/project
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 /path/to/your/project/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. 启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start scriptwriter
sudo systemctl enable scriptwriter
```

3. 配置 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. 重启 Nginx：

```bash
sudo systemctl restart nginx
```

---

### 方式 6：PythonAnywhere（免费额度）

1. 注册 [PythonAnywhere](https://www.pythonanywhere.com)
2. 创建 "Web" 应用
3. 选择 "Flask" 框架
4. 上传代码文件
5. 配置 `requirements.txt`
6. 启动应用

---

## 🔧 本地测试

在部署前，您可以在本地测试：

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行服务

```bash
python app.py
```

服务将在 http://localhost:5000 运行

---

## 🎯 首次使用

1. **访问链接**：打开部署后的链接（例如 https://scriptwriter-cloud.vercel.app）
2. **设置 Token**：
   - 点击左侧的 "⚙️ Token 设置" 按钮
   - 或者访问 https://your-domain.com/settings
   - 输入您的 Coze API Token（在 https://coze.com/user/pat 获取）
3. **开始使用**：Token 保存后，就可以正常使用了

---

## 📱 多设备使用

云端部署支持多设备访问：

1. **手机访问**：在手机浏览器输入部署链接
2. **Token 同步**：不同设备需要分别设置 Token
3. **对话隔离**：每个设备的对话历史独立存储
4. **随时访问**：只要有网络，任何地方都能使用

---

## 🔒 安全提示

1. **Token 安全**：
   - Token 保存在云端服务器，不会泄露给第三方
   - 请妥善保管您的 Token，不要分享给他人

2. **HTTPS 加密**：
   - Vercel/Railway/Render 等平台自动提供 HTTPS
   - 如果使用自己的服务器，需要配置 SSL 证书

3. **访问控制**：
   - 当前版本开放访问，任何人都可以使用
   - 如需添加登录验证，可以基于 device_id 实现

---

## 💡 常见问题

### Q: 部署后无法访问？

A: 检查以下几点：
1. 部署日志是否有错误
2. 依赖包是否正确安装
3. 端口是否正确配置（Flask 默认 5000）
4. 防火墙是否允许访问

### Q: Token 提示无效？

A: 确认以下几点：
1. Token 格式是否正确（以 pat_ 开头）
2. Token 是否已过期
3. Token 是否有足够权限

### Q: 对话历史丢失？

A: 检查以下几点：
1. 云端服务是否正常运行
2. data/ 目录是否有写权限
3. Token 是否正确

### Q: 如何更新代码？

A: 不同平台方式不同：
- Vercel: `vercel --prod`
- Railway: `railway up`
- Render: 推送代码到 GitHub，自动部署
- 自己的服务器: `git pull` 然后 `sudo systemctl restart scriptwriter`

---

## 🆘 技术支持

如果遇到问题：

1. 查看部署平台日志
2. 检查服务器日志：`tail -f /path/to/logs/app.log`
3. 在本地测试是否正常
4. 联系平台技术支持

---

## 📌 推荐方案

**个人使用**：Vercel（免费、简单、快速）
**商业使用**：阿里云/腾讯云 + Nginx（稳定、可控）
**团队协作**：Railway（团队管理方便）

祝您部署顺利！🚀
