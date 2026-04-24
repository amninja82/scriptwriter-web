@echo off
chcp 65001
echo ========================================
echo 多智能体编剧系统 - 打包工具
echo ========================================
echo.

echo [1/4] 检查 Python...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/4] 安装依赖...
pip install -r gui_requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)
echo.

echo [3/4] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo.

echo [4/4] 开始打包（这可能需要几分钟）...
pyinstaller --onefile --windowed --name="多智能体编剧系统" --icon=icon.ico scriptwriter_gui.py
if errorlevel 1 (
    echo 错误: 打包失败
    pause
    exit /b 1
)
echo.

echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 可执行文件位置: dist\多智能体编剧系统.exe
echo.
echo 双击运行即可使用！
echo.
pause
