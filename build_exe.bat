@echo off
chcp 65001
echo ========================================
echo 多智能体编剧系统 - 打包工具
echo ========================================
echo.

echo [1/5] 检查 Python...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/5] 安装依赖（用户级，无需管理员权限）...
pip install --user -r gui_requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    echo.
    echo 提示：如果仍然失败，请尝试：
    echo 1. 右键点击 build_exe.bat，选择"以管理员身份运行"
    echo 2. 或手动安装：pip install --user pyinstaller requests
    pause
    exit /b 1
)
echo.

echo [3/5] 获取 Python 用户包路径...
for /f "delims=" %%i in ('python -m site --user-site') do set USER_SITE=%%i
echo 用户包路径: %USER_SITE%
echo.

echo [4/5] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo.

echo [5/5] 开始打包（这可能需要几分钟）...
pyinstaller --onefile --windowed --name="多智能体编剧系统" --paths="%USER_SITE%" scriptwriter_gui.py
if errorlevel 1 (
    echo 错误: 打包失败
    echo.
    echo 提示：请检查 pyinstaller 是否已正确安装
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
