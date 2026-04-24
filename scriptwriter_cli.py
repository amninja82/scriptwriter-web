#!/usr/bin/env python3
"""
多智能体编剧系统 - 命令行版本
直接在终端中使用，无需浏览器
"""

import requests
import json

# 配置
API_URL = 'https://2km4yszdhf.coze.site/stream_run'
PROJECT_ID = 7632132891593703478

class ScriptwriterCLI:
    def __init__(self):
        self.api_token = ''
        self.session_id = ''
        self.connected = False

    def print_banner(self):
        """打印欢迎横幅"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎭 多智能体编剧系统 - 命令行版本                        ║
║                                                           ║
║   7个专业编剧智能体协作，为您打造精品剧本                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(banner)

    def connect(self):
        """连接到智能体"""
        print("\n📝 请输入您的 API Token:")
        print("(提示：在部署界面的 Header 参数区点击 'API Token' 按钮获取)\n")

        # 隐藏输入（密码模式）
        import getpass
        self.api_token = getpass.getpass("API Token: ").strip()

        if not self.api_token:
            print("❌ 未输入 API Token，连接失败")
            return False

        # 生成会话ID
        import time
        import random
        import string
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
        self.session_id = f"cli_session_{int(time.time())}_{random_str}"

        print("\n🔄 正在连接智能体...")

        try:
            # 发送测试消息
            response = self.send_message_to_api("你好", is_test=True)

            if response:
                self.connected = True
                print("✅ 连接成功！\n")
                print("=" * 60)
                print("🤖 智能体:")
                print(response)
                print("=" * 60)
                print("\n💡 提示：")
                print("  - 输入消息开始对话")
                print("  - 输入 'quit' 或 'exit' 退出")
                print("  - 输入 'clear' 清空屏幕")
                print("  - 输入 'help' 查看帮助\n")
                return True
            else:
                print("❌ 连接失败，未收到响应")
                return False

        except Exception as e:
            print(f"❌ 连接失败: {str(e)}")
            return False

    def send_message_to_api(self, text, is_test=False):
        """发送消息到API"""
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'content': {
                'query': {
                    'prompt': [
                        {
                            'type': 'text',
                            'content': {
                                'text': text
                            }
                        }
                    ]
                }
            },
            'type': 'query',
            'session_id': self.session_id,
            'project_id': PROJECT_ID
        }

        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                stream=True,
                timeout=60
            )

            if response.status_code != 200:
                if response.status_code == 401:
                    raise Exception("API Token 无效，请检查 Token 是否正确")
                elif response.status_code == 429:
                    raise Exception("请求过于频繁，请稍后再试")
                else:
                    raise Exception(f"HTTP 错误: {response.status_code}")

            # 读取流式响应
            full_response = ''
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if data.get('content'):
                            content = data['content']
                            full_response += content
                            if not is_test:
                                # 实时显示（可选）
                                pass
                    except json.JSONDecodeError:
                        pass

            return full_response

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求错误: {str(e)}")
        except Exception as e:
            raise e

    def send_message(self, text):
        """发送消息并显示响应"""
        if not self.connected:
            print("❌ 未连接，请先运行 connect() 方法")
            return

        # 显示用户消息
        print(f"\n{'=' * 60}")
        print("📝 你:")
        print(text)
        print("=" * 60)

        # 发送消息
        try:
            response = self.send_message_to_api(text)

            # 显示智能体回复
            print(f"\n🤖 智能体:")
            print(response)
            print("\n" + "=" * 60)

        except Exception as e:
            print(f"\n❌ 发送失败: {str(e)}")
            print("=" * 60)

    def show_help(self):
        """显示帮助信息"""
        help_text = """
╔═══════════════════════════════════════════════════════════╗
║                    📚 帮助信息                            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  基本命令：                                               ║
║    - 输入任何文本开始对话                                ║
║    - quit / exit     退出程序                            ║
║    - clear            清空屏幕                            ║
║    - help             显示帮助                            ║
║                                                           ║
║  常用对话示例：                                           ║
║    - 你好，请介绍一下你自己                               ║
║    - 创建一个电视剧项目                                   ║
║    - 查看所有项目                                         ║
║    - 搜索悬疑剧的经典剧情结构                             ║
║    - 帮我构思一个关于时间旅行的故事                       ║
║                                                           ║
║  功能说明：                                               ║
║    - 创建和管理剧本项目                                   ║
║    - 7个专业编剧智能体协作                                ║
║    - 知识库搜索和联网搜索                                 ║
║    - 项目历史管理                                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(help_text)

    def run(self):
        """运行交互式界面"""
        self.print_banner()

        # 连接到智能体
        if not self.connect():
            print("\n❌ 无法连接，程序退出")
            return

        # 进入交互模式
        while True:
            try:
                # 获取用户输入
                user_input = input("\n💬 请输入消息 (输入 'quit' 退出): ").strip()

                if not user_input:
                    continue

                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 感谢使用，再见！")
                    break
                elif user_input.lower() == 'clear':
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                    continue
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue

                # 发送消息
                self.send_message(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 感谢使用，再见！")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {str(e)}")


def main():
    """主函数"""
    cli = ScriptwriterCLI()
    cli.run()


if __name__ == "__main__":
    main()
