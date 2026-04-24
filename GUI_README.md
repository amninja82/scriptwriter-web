# 多智能体编剧系统 - 本地 GUI 版本

## 📖 简介

这是一个基于 Python Tkinter 开发的本地图形界面应用，无需网络部署，直接在本地运行。

## ✨ 功能特点

- ✅ **聊天界面**：类似微信的聊天界面，易用友好
- ✅ **Token 管理**：本地保存，安全可靠
- ✅ **对话历史**：自动保存，下次打开自动加载
- ✅ **无需 VPN**：完全本地运行，无网络限制
- ✅ **跨平台**：支持 Windows、Mac、Linux

## 🚀 快速开始

### 方式 1：使用已打包的 exe（推荐）

1. **下载 exe 文件**
   - 找到 `dist/多智能体编剧系统.exe`
   - 下载到任意位置

2. **运行**
   - 双击 `多智能体编剧系统.exe`
   - 首次运行会提示设置 Token

3. **配置 Token**
   - 点击菜单"设置" → "Token 设置"
   - 输入您的 Coze API Token
   - 点击"保存"

4. **开始使用**
   - 在输入框输入消息
   - 点击"发送"或按回车
   - 开始聊天！

---

### 方式 2：自己打包

#### Windows 用户：

1. **安装 Python**
   - 下载：https://www.python.org/downloads/
   - 安装时勾选"Add Python to PATH"

2. **安装依赖**
   ```bash
   pip install -r gui_requirements.txt
   ```

3. **运行打包脚本**
   ```bash
   build_exe.bat
   ```

4. **运行 exe**
   - 在 `dist` 目录找到 `多智能体编剧系统.exe`
   - 双击运行

#### Mac/Linux 用户：

1. **安装 Python**
   ```bash
   # Mac
   brew install python3

   # Linux
   sudo apt install python3
   ```

2. **安装依赖**
   ```bash
   pip3 install -r gui_requirements.txt
   ```

3. **运行打包脚本**
   ```bash
   chmod +x build_exe.sh
   ./build_exe.sh
   ```

4. **运行**
   ```bash
   ./dist/多智能体编剧系统
   ```

---

### 方式 3：直接运行源码

1. **安装依赖**
   ```bash
   pip install -r gui_requirements.txt
   ```

2. **运行**
   ```bash
   python scriptwriter_gui.py
   ```

---

## 📋 使用说明

### 主界面

**顶部菜单栏：**
- **文件**
  - 清空对话：清除对话历史
  - 退出：关闭应用
- **设置**
  - Token 设置：配置 API Token
  - 关于：查看版本信息

**对话区域：**
- 蓝色：您的消息
- 绿色：助手的回复

**输入区域：**
- 输入框：输入消息
- 发送按钮：点击发送（或按回车）

### Token 设置

**如何获取 Token：**

1. 访问 Coze 平台：https://coze.com/user/pat
2. 创建新的 Personal Access Token
3. 复制 Token

**设置 Token：**

1. 点击菜单"设置" → "Token 设置"
2. 粘贴 Token
3. 点击"保存"

### 对话历史

**自动保存：**
- 每次对话自动保存到本地
- 下次打开自动加载

**清空对话：**
- 点击菜单"文件" → "清空对话"
- 确认后清空所有历史

---

## 🔧 配置文件

应用会自动创建以下文件：

- `config.json`：保存 Token 和设备 ID
- `chat_history_*.json`：保存对话历史

**文件位置：**
- 和 exe 文件在同一目录

---

## 💡 常见问题

### Q1: Token 保存不了？

**A:** 检查是否有权限创建文件，确保 exe 所在目录可写。

---

### Q2: 无法连接服务器？

**A:**
1. 检查 Token 是否正确
2. 检查网络连接
3. 检查 Coze 平台是否正常

---

### Q3: 打包后文件太大？

**A:**
- 使用 `--onefile` 模式会包含所有依赖
- 可以尝试使用 `--onedir` 模式减小体积

---

### Q4: Mac/Linux 打包失败？

**A:**
- 确保安装了 pyinstaller
- 使用 `pip3 install pyinstaller`

---

## 🎯 技术栈

- **GUI 框架**: Python Tkinter
- **HTTP 请求**: requests
- **打包工具**: PyInstaller

---

## 📦 文件说明

```
├── scriptwriter_gui.py      # 主程序
├── gui_requirements.txt     # 依赖列表
├── build_exe.bat            # Windows 打包脚本
├── build_exe.sh             # Mac/Linux 打包脚本
├── GUI_README.md            # 使用说明（本文件）
└── dist/                    # 打包输出目录
    └── 多智能体编剧系统.exe  # 可执行文件
```

---

## 🆘 技术支持

如果遇到问题：

1. 查看本文档的"常见问题"部分
2. 检查错误日志
3. 联系技术支持

---

## 📝 更新日志

### v1.0.0 (2024-04-24)
- ✅ 初始版本发布
- ✅ 基础聊天功能
- ✅ Token 管理
- ✅ 对话历史保存

---

## 🎉 享受使用！

感谢您使用多智能体编剧系统！

如有任何问题或建议，欢迎反馈！
