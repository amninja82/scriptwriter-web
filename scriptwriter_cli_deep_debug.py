#!/usr/bin/env python3
"""
多智能体编剧系统 - 命令行版本（深度调试版）
显示服务器返回的原始数据
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
║   🎭 多智能体编剧系统 - 命令行版本（深度调试版）           ║
║                                                           ║
║   7个专业编剧智能体协作，为您打造精品剧本                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(banner)

    def get_input(self, prompt):
        """获取用户输入"""
        try:
            return input(prompt)
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
            return None
        except Exception as e:
            print(f"\n❌ 输入错误: {str(e)}")
            return None

    def connect(self):
        """连接到智能体"""
        print("\n📝 请输入您的 API Token:")
        print("(提示：在部署界面的 Header 参数区点击 'API Token' 按钮获取)")
        print("(注意：输入时会显示在屏幕上，请确保周围无人查看)")
        print("\n操作提示：")
        print("  1. 从部署界面复制 Token (Ctrl+C)")
        print("  2. 在这里右键点击，选择'粘贴'")
        print("  3. 或者按 Shift+Insert 粘贴")
        print("  4. 粘贴后按回车确认\n")

        self.api_token = self.get_input("API Token: ")

        if not self.api_token:
            print("❌ 未输入 API Token，连接失败")
            return False

        self.api_token = self.api_token.strip()

        # 生成会话ID
        import time
        import random
        import string
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
        self.session_id = f"cli_session_{int(time.time())}_{random_str}"

        print("\n🔄 正在连接智能体...")
        print(f"📍 API 地址: {API_URL}")
        print(f"🆔 会话 ID: {self.session_id}")

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
            print("\n📋 可能的原因：")
            print("  1. API Token 无效或过期")
            print("  2. 网络连接问题")
            print("  3. API 服务器返回格式异常")
            print("\n💡 建议操作：")
            print("  - 检查 Token 是否正确复制")
            print("  - 尝试重新获取 Token")
            print("  - 查看上面的调试信息")
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
            if not is_test:
                print("⏳ 等待响应...")
            else:
                print(f"📤 发送测试消息: {text}")
                print(f"📦 请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}")

            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                stream=True,
                timeout=60
            )

            print(f"📊 响应状态码: {response.status_code}")

            if response.status_code != 200:
                if response.status_code == 401:
                    raise Exception("API Token 无效，请检查 Token 是否正确")
                elif response.status_code == 429:
                    raise Exception("请求过于频繁，请稍后再试")
                else:
                    error_msg = f"HTTP 错误: {response.status_code}"
                    try:
                        error_detail = response.text
                        error_msg += f"\n响应内容: {error_detail}"
                    except:
                        pass
                    raise Exception(error_msg)

            # 读取流式响应
            print("📖 开始读取流式响应...")
            full_response = ''
            line_count = 0
            content_lines = 0
            first_5_lines = []
            last_5_lines = []

            for line in response.iter_lines():
                line_count += 1
                if line:
                    line_str = line.decode('utf-8')

                    # 保存前5行和后5行
                    if line_count <= 5:
                        first_5_lines.append(line_str)
                    if line_count > line_count - 5:
                        last_5_lines.append(line_str)

                    # 显示前10行
                    if line_count <= 10:
                        print(f"\n  行 {line_count} (原始): {line_str}")

                    try:
                        data = json.loads(line_str)

                        # 打印 JSON 结构（前3行）
                        if line_count <= 3:
                            print(f"  行 {line_count} (JSON键): {list(data.keys())}")

                        if data.get('content'):
                            content = data['content']
                            full_response += content
                            content_lines += 1
                            if not is_test and content_lines <= 3:
                                print(f"  ✅ 第 {content_lines} 个 content 片段: {content[:50]}...")
                        else:
                            # 打印非 content 的数据
                            if line_count <= 3:
                                print(f"  ⚠️ 行 {line_count} 没有 content 字段，包含: {list(data.keys())}")
                    except json.JSONDecodeError as e:
                        if line_count <= 3:
                            print(f"  ⚠️ 行 {line_count} JSON 解析失败: {e}")
                            print(f"  原始内容: {line_str}")
                        pass

            print(f"\n📊 统计信息:")
            print(f"  总行数: {line_count}")
            print(f"  包含 content 的行数: {content_lines}")
            print(f"  响应长度: {len(full_response)} 字符")

            # 如果没有 content，显示前5行和后5行
            if not full_response:
                print(f"\n⚠️ 未找到 content 字段，显示前5行:")
                for i, line in enumerate(first_5_lines, 1):
                    print(f"  第 {i} 行: {line}")

                print(f"\n⚠️ 显示后5行:")
                for i, line in enumerate(last_5_lines, len(last_5_lines) - 4):
                    print(f"  第 {i} 行: {line}")

                raise Exception("服务器未返回有效响应内容")

            return full_response

        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接错误，请检查是否能访问互联网")
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
            input("\n按回车键退出...")
            return

        # 进入交互模式
        while True:
            try:
                # 获取用户输入
                user_input = self.get_input("\n💬 请输入消息 (输入 'quit' 退出): ")

                if user_input is None:
                    # 用户按了 Ctrl+C
                    print("\n👋 感谢使用，再见！")
                    break

                user_input = user_input.strip()

                if not user_input:
                    continue

                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', 'q']:
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
                # 继续运行，不退出程序


def main():
    """主函数"""
    cli = ScriptwriterCLI()
    cli.run()


if __name__ == "__main__":
    main()
