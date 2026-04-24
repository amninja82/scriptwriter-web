#!/usr/bin/env python3
"""
Vercel 快速部署脚本
使用方法：python deploy_to_vercel.py
"""

import os
import subprocess
import sys

def run_command(cmd, description=""):
    """执行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    print(f"执行命令: {cmd}\n")

    result = subprocess.run(cmd, shell=True, capture_output=False)

    if result.returncode != 0:
        print(f"❌ 错误: 命令执行失败")
        return False

    print(f"✅ {description} 完成")
    return True

def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║         多智能体编剧系统 - Vercel 部署工具          ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # 步骤 1: 检查必要文件
    print("\n📁 检查必要文件...")

    required_files = [
        'app.py',
        'requirements.txt',
        'vercel.json',
        'scriptwriter_cloud.html',
        'scriptwriter_settings.html'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            print(f"❌ 缺少文件: {file}")
        else:
            print(f"✅ {file}")

    if missing_files:
        print(f"\n❌ 缺少必要文件: {', '.join(missing_files)}")
        print("请先确保所有文件都存在！")
        sys.exit(1)

    # 步骤 2: 检查 Git 仓库
    print("\n🔍 检查 Git 仓库...")

    if not os.path.exists('.git'):
        print("⚠️  未检测到 Git 仓库，正在初始化...")

        if not run_command("git init", "初始化 Git 仓库"):
            sys.exit(1)

        if not run_command("git add .", "添加所有文件"):
            sys.exit(1)

        if not run_command('git commit -m "初始化编剧智能体网页版"', "提交代码"):
            sys.exit(1)
    else:
        print("✅ Git 仓库已存在")

    # 步骤 3: 检查远程仓库
    print("\n🔗 检查远程仓库...")

    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    remotes = result.stdout.strip()

    if not remotes or "origin" not in remotes:
        print("\n⚠️  未检测到远程仓库")
        print("\n请按以下步骤操作：")
        print("1. 访问 https://github.com/new")
        print("2. 创建一个新的仓库")
        print("3. 复制仓库 URL（格式: https://github.com/用户名/仓库名.git）")
        print("4. 运行以下命令：")
        print("   git remote add origin <你的仓库URL>")
        print("   git branch -M main")
        print("   git push -u origin main")
        print("\n完成后，继续部署到 Vercel：")
        print("   vercel login")
        print("   vercel")
        print("   vercel --prod")
        sys.exit(0)
    else:
        print(f"✅ 远程仓库已配置:\n{remotes}")

    # 步骤 4: 检查 Vercel CLI
    print("\n🚀 检查 Vercel CLI...")

    result = subprocess.run("vercel --version", shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Vercel CLI 未安装")
        print("\n请先安装 Vercel CLI：")
        print("   npm install -g vercel")
        print("\n安装完成后，重新运行此脚本。")
        sys.exit(1)
    else:
        print(f"✅ Vercel CLI 已安装: {result.stdout.strip()}")

    # 步骤 5: 检查 Vercel 登录状态
    print("\n🔐 检查 Vercel 登录状态...")

    result = subprocess.run("vercel whoami", shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ 未登录 Vercel")
        print("\n请先登录：")
        print("   vercel login")
        print("\n登录完成后，重新运行此脚本。")
        sys.exit(1)
    else:
        print(f"✅ 已登录 Vercel: {result.stdout.strip()}")

    # 步骤 6: 提交最新更改
    print("\n💾 提交最新更改...")

    if not run_command("git add .", "添加所有文件"):
        sys.exit(1)

    commit_msg = "更新: 准备部署到 Vercel"
    if not run_command(f'git commit -m "{commit_msg}"', "提交代码"):
        print("⚠️  没有新的更改需要提交")

    # 步骤 7: 推送到 GitHub
    print("\n⬆️  推送到 GitHub...")

    result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True)
    current_branch = result.stdout.strip()

    if not current_branch:
        if not run_command("git branch -M main", "设置主分支为 main"):
            sys.exit(1)

    if not run_command(f"git push -u origin {current_branch or 'main'}", "推送代码"):
        sys.exit(1)

    # 步骤 8: 部署到 Vercel
    print("\n🚀 部署到 Vercel...")

    if not run_command("vercel", "部署到 Vercel（预览版）"):
        sys.exit(1)

    # 步骤 9: 正式部署
    print("\n🎯 正式部署...")

    if not run_command("vercel --prod", "正式部署到 Vercel"):
        sys.exit(1)

    # 完成
    print(f"""
    {'='*60}
    🎉 部署完成！
    {'='*60}

    ✅ 您的网页版已成功部署到 Vercel！

    下一步：
    1. 查看部署链接，访问您的网页版
    2. 打开 Token 设置页面，配置 Coze API Token
    3. 开始使用编剧智能体！

    如需查看部署日志，运行：
       vercel logs

    如需更新部署，运行：
       git add .
       git commit -m "更新说明"
       git push
       vercel --prod

    祝您使用愉快！🚀
    """)

if __name__ == "__main__":
    main()
