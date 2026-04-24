# Vercel 项目优化清单

## 当前状态
- ✅ 代码已推送到 GitHub
- ✅ Git 仓库: https://github.com/amninja82/scriptwriter-web.git
- ✅ 代码已更新（包含所有修复）

## 需要您完成的任务

### 任务 1：识别项目
在 Vercel Dashboard 中：
- [ ] 打开 https://vercel.com/dashboard
- [ ] 列出 3 个项目的名称
- [ ] 确定哪个是正式项目（最新的、能访问的）

### 任务 2：配置 Git 自动部署
在正式项目中：
- [ ] 进入项目
- [ ] 点击 Settings → Git
- [ ] 确认已绑定 `amninja82/scriptwriter-web` 仓库
- [ ] 启用 Automatic Deployments

### 任务 3：删除旧项目
- [ ] 删除 2 个旧项目
- [ ] 只保留 1 个正式项目

### 任务 4：测试自动部署
- [ ] 修改一个文件（比如 README）
- [ ] 提交并推送：
  ```bash
  git add README.md
  git commit -m "test"
  git push
  ```
- [ ] 等待 Vercel 自动部署
- [ ] 验证部署成功

## 完成！

配置完成后，以后只需：
1. 修改代码
2. `git push`
3. Vercel 自动部署 ✅
