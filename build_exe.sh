#!/bin/bash

echo "========================================"
echo "多智能体编剧系统 - 打包工具"
echo "========================================"
echo ""

echo "[1/4] 检查 Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi
echo ""

echo "[2/4] 安装依赖..."
pip3 install -r gui_requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 依赖安装失败"
    exit 1
fi
echo ""

echo "[3/4] 清理旧的打包文件..."
rm -rf build dist *.spec
echo ""

echo "[4/4] 开始打包（这可能需要几分钟）..."
pyinstaller --onefile --windowed --name="多智能体编剧系统" scriptwriter_gui.py
if [ $? -ne 0 ]; then
    echo "错误: 打包失败"
    exit 1
fi
echo ""

echo "========================================"
echo "打包完成！"
echo "========================================"
echo ""
echo "可执行文件位置: dist/多智能体编剧系统"
echo ""
echo "双击运行即可使用！"
echo ""
