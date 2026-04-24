# 多智能体编剧系统 - Windows 打包指南

## 📦 一键打包步骤

### 1. 安装 Python

如果您还没有安装 Python：

1. 访问：https://www.python.org/downloads/
2. 下载 Python 3.10 或更高版本
3. 安装时**必须勾选** "Add Python to PATH"
4. 完成安装

### 2. 安装依赖

打开 CMD（按 Win + R，输入 cmd，回车），运行：

```bash
pip install pyinstaller requests
```

### 3. 下载文件

从 Coze Coding 下载以下两个文件到同一个文件夹（如 `C:\Scriptwriter\`）：

- `scriptwriter_cli_fixed.py`
- `scriptwriter.spec`

### 4. 打包成 exe

打开 CMD，进入文件所在目录：

```bash
cd C:\Scriptwriter\
```

运行打包命令：

```bash
pyinstaller scriptwriter.spec
```

或者使用简化命令：

```bash
pyinstaller --onefile --name "多智能体编剧系统" --clean scriptwriter_cli_fixed.py
```

### 5. 获取 exe 文件

打包成功后，exe 文件在：

```
C:\Scriptwriter\dist\多智能体编剧系统.exe
```

双击即可运行！

---

## 🎯 打包参数说明

```bash
pyinstaller --onefile --name "多智能体编剧系统" --clean scriptwriter_cli_fixed.py
```

- `--onefile`: 打包成单个 exe 文件
- `--name "多智能体编剧系统"`: 指定输出文件名
- `--clean`: 清理缓存
- `scriptwriter_cli_fixed.py`: 要打包的脚本

---

## ⚠️ 可能遇到的问题

### 问题1：找不到 pyinstaller

**错误**：
```
'pyinstaller' 不是内部或外部命令
```

**解决**：
```bash
python -m pip install pyinstaller
```

### 问题2：找不到 requests

**错误**：
```
ModuleNotFoundError: No module named 'requests'
```

**解决**：
```bash
pip install requests
```

### 问题3：打包失败

**解决**：
```bash
# 清理缓存后重试
pyinstaller --clean --onefile --name "多智能体编剧系统" scriptwriter_cli_fixed.py
```

---

## 📱 使用 exe 文件

### 双击运行

```
1. 双击 "多智能体编剧系统.exe"
2. 看到欢迎界面
3. 输入 API Token
4. 开始使用！
```

### 创建快捷方式

```
1. 右键点击 exe 文件
2. 选择 "发送到" → "桌面快捷方式"
3. 以后可以从桌面直接启动
```

---

## 🔐 关于 Token 显示

由于 Windows 兼容性问题，输入 Token 时会显示在屏幕上。

**安全建议**：
- 确保周围没有人看您的屏幕
- 输入完 Token 后立即按回车
- 不要分享您的 Token

---

## 📊 文件大小

打包后的 exe 文件大约 15-20MB，包含：
- Python 运行时
- 所有依赖库
- 您的脚本

---

## 🎉 完成后

打包成功后，您将拥有：

✅ 独立的可执行文件
✅ 无需安装 Python
✅ 双击即可运行
✅ 无需 Coze 和 VPN
✅ 功能完整

---

## 📞 需要帮助？

如果在打包过程中遇到问题，请：

1. 复制完整的错误信息
2. 告诉我您在哪一步失败
3. 我会提供详细的解决方案

---

**祝您打包顺利！** 🚀
