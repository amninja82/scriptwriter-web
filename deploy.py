#!/usr/bin/env python3
"""
一键部署脚本 - PythonAnywhere
快速将编剧系统部署到云端
"""

import os
import sys
import subprocess

def print_step(step, message):
    """打印步骤"""
    print(f"\n{'='*60}")
    print(f"步骤 {step}: {message}")
    print(f"{'='*60}\n")

def run_command(command, description):
    """执行命令"""
    print(f"执行: {description}")
    print(f"命令: {command}\n")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} 成功\n")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败")
        print(f"错误: {e.stderr}\n")
        return False

def check_files():
    """检查必要文件"""
    print_step(1, "检查文件完整性")

    required_files = [
        'app.py',
        'scriptwriter_cloud.html',
        'scriptwriter_settings.html',
        'requirements.txt'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ 缺少以下文件:")
        for file in missing_files:
            print(f"  - {file}")
        print("\n请确保所有文件都存在后再继续")
        return False

    print("✅ 所有必要文件都存在\n")
    return True

def install_dependencies():
    """安装依赖"""
    print_step(2, "安装 Python 依赖")

    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt 不存在")
        return False

    success = run_command(
        "pip install -r requirements.txt",
        "安装依赖包"
    )

    return success

def create_data_directory():
    """创建数据目录"""
    print_step(3, "创建数据目录")

    if not os.path.exists('data'):
        os.makedirs('data')
        print("✅ 创建 data 目录\n")
    else:
        print("✅ data 目录已存在\n")

    return True

def test_locally():
    """本地测试"""
    print_step(4, "本地测试")

    print("启动 Flask 服务...")
    print("服务将在 http://localhost:5000 运行")
    print("按 Ctrl+C 停止服务\n")

    try:
        subprocess.run(
            ["python", "app.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n✅ 本地测试完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 本地测试失败: {e}")
        return False

def generate_vercel_config():
    """生成 Vercel 配置"""
    print_step(5, "生成 Vercel 配置")

    vercel_json = {
        "version": 2,
        "builds": [
            {
                "src": "app.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/app.py"
            }
        ]
    }

    with open('vercel.json', 'w') as f:
        import json
        json.dump(vercel_json, f, indent=2)

    print("✅ 生成 vercel.json 配置文件\n")
    return True

def deploy_vercel():
    """部署到 Vercel"""
    print_step(6, "部署到 Vercel")

    # 检查是否安装了 Vercel CLI
    try:
        subprocess.run(
            ["vercel", "--version"],
            check=True,
            capture_output=True
        )
        print("✅ Vercel CLI 已安装\n")
    except subprocess.CalledProcessError:
        print("❌ 未检测到 Vercel CLI")
        print("\n请先安装 Vercel CLI:")
        print("  npm install -g vercel")
        print("\n然后重新运行此脚本")
        return False

    # 检查是否已登录
    print("检查 Vercel 登录状态...")
    if not run_command("vercel whoami", "检查登录"):
        print("\n请先登录 Vercel:")
        print("  vercel login")
        print("\n然后重新运行此脚本")
        return False

    # 部署
    print("\n开始部署到 Vercel...")
    print("这可能需要几分钟时间，请耐心等待\n")

    success = run_command("vercel --prod", "部署")

    if success:
        print("\n" + "="*60)
        print("🎉 部署成功！")
        print("="*60)
        print("\n您的应用已部署到云端")
        print("请查看上方的访问链接")
        print("\n首次使用:")
        print("1. 访问部署链接")
        print("2. 点击左侧 '⚙️ Token 设置'")
        print("3. 输入您的 Coze API Token")
        print("4. 开始使用！")
        print("="*60 + "\n")

    return success

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 多智能体编剧系统 - 云端部署工具")
    print("="*60 + "\n")

    print("本工具将帮助您将编剧系统部署到云端")
    print("推荐使用 Vercel（免费、快速）")
    print("\n")

    if not check_files():
        return 1

    if not install_dependencies():
        return 1

    if not create_data_directory():
        return 1

    print_step(4, "选择部署方式")
    print("请选择部署方式:")
    print("  1. 本地测试")
    print("  2. 部署到 Vercel（推荐）")
    print("  3. 查看部署指南")

    choice = input("\n请输入选择 (1/2/3): ").strip()

    if choice == '1':
        test_locally()
    elif choice == '2':
        if not generate_vercel_config():
            return 1
        if not deploy_vercel():
            return 1
    elif choice == '3':
        print("\n请查看 CLOUD_DEPLOYMENT_GUIDE.md 了解详细部署指南\n")
    else:
        print("\n❌ 无效选择\n")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
