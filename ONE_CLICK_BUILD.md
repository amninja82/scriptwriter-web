# 一键打包命令（PowerShell）

## 🚀 最简单的一键打包命令

```powershell
cd C:\Users\Admin\Desktop\Scriptwriter; python -m PyInstaller --onefile --name "多智能体编剧系统" --clean scriptwriter_cli_windows.py
```

---

## 📋 使用步骤

### 1. 确保文件已下载

确保 `scriptwriter_cli_windows.py` 已下载到：
```
C:\Users\Admin\Desktop\Scriptwriter\
```

### 2. 打开 PowerShell

按 Win + X，选择"Windows PowerShell"

### 3. 复制并运行以下命令

```powershell
cd C:\Users\Admin\Desktop\Scriptwriter; python -m PyInstaller --onefile --name "多智能体编剧系统" --clean scriptwriter_cli_windows.py
```

### 4. 等待打包完成

打包完成后，exe 文件在：
```
C:\Users\Admin\Desktop\Scriptwriter\dist\多智能体编剧系统.exe
```

### 5. 运行测试

```powershell
C:\Users\Admin\Desktop\Scriptwriter\dist\多智能体编剧系统.exe
```

---

## ✅ 完成！

现在新版本应该可以正常输入和粘贴 Token 了！
