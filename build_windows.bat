@echo off
REM 一键打包脚本 - Windows
REM 将 Python 脚本打包为 Windows exe

echo ========================================
echo   多智能体编剧系统 - 打包工具
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
if not exist "scriptwriter_cli_final.py" (
    echo [错误] 找不到 scriptwriter_cli_final.py
    pause
    exit /b 1
)

echo [4/5] 打包脚本为 exe...
echo 这可能需要几分钟，请耐心等待...
echo.

pyinstaller --onefile --name "编剧智能体" --icon=NONE --clean scriptwriter_cli_final.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo [5/5] 清理临时文件...
if exist "build" rmdir /s /q build
if exist "scriptwriter_cli_final.spec" del /f /q scriptwriter_cli_final.spec

echo.
echo ========================================
echo   ✅ 打包成功！
echo ========================================
echo.
echo exe 文件位置: dist\编剧智能体.exe
echo.
echo 使用方法:
echo   1. 双击运行 dist\编剧智能体.exe
echo   2. 输入您的 API Token
echo   3. 开始使用！
echo.
echo 提示:
echo   - 可以将 exe 文件复制到任何位置
echo   - 不需要安装 Python
echo   - 复杂任务可能需要 1-2 分钟处理，请耐心等待
echo.
pause
