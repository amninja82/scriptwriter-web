@echo off
REM 一键打包脚本 - Windows GUI 版本

echo ========================================
echo   多智能体编剧系统 - GUI 版打包工具
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] 检查 Python 版本...
python --version
echo.

REM 检查 pip 是否可用
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] pip 不可用
    pause
    exit /b 1
)

echo [2/5] 检查 pip...
pip --version
echo.

REM 安装 PyInstaller
echo [3/5] 安装/更新 PyInstaller...
pip install pyinstaller --upgrade
echo.

REM 检查源文件是否存在
if not exist "scriptwriter_gui.py" (
    echo [错误] 找不到 scriptwriter_gui.py
    pause
    exit /b 1
)

echo [4/5] 打包 GUI 版本为 exe...
echo 这可能需要几分钟，请耐心等待...
echo.

pyinstaller --onefile --windowed --name "编剧智能体-GUI" --icon=NONE --clean scriptwriter_gui.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo [5/5] 清理临时文件...
if exist "build" rmdir /s /q build
if exist "scriptwriter_gui.spec" del /f /q scriptwriter_gui.spec

echo.
echo ========================================
echo   ✅ 打包成功！
echo ========================================
echo.
echo exe 文件位置: dist\编剧智能体-GUI.exe
echo.
echo 使用方法:
echo   1. 双击运行 dist\编剧智能体-GUI.exe
echo   2. 点击 "⚙️ 设置 Token" 输入 Coze API Token
echo   3. 创建项目开始使用！
echo.
echo 功能特点:
echo   - 图形界面，操作简单
echo   - 项目管理，对话历史本地存储
echo   - 联网搜索，自动保存到知识库
echo   - 支持导出对话记录
echo.
pause
