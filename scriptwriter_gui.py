import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import os
from datetime import datetime
import threading

class ScriptWriterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("多智能体编剧系统")
        self.root.geometry("900x700")

        # 配置
        self.API_URL = 'https://2km4yszdhf.coze.site/stream_run'
        self.PROJECT_ID = 7632132891593703478
        self.config_file = 'config.json'

        # 加载配置
        self.load_config()

        # 创建界面
        self.create_widgets()

        # 加载对话历史
        self.load_chat_history()

    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.token = config.get('token', '')
                self.device_id = config.get('device_id', 'device_default')
        else:
            self.token = ''
            self.device_id = 'device_default'

    def save_config(self):
        """保存配置"""
        config = {
            'token': self.token,
            'device_id': self.device_id
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def load_chat_history(self):
        """加载对话历史"""
        self.history_file = f'chat_history_{self.device_id}.json'
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
        else:
            self.chat_history = []

        # 显示对话历史
        self.display_chat_history()

    def save_chat_history(self):
        """保存对话历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        """创建界面组件"""
        # 顶部菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="清空对话", command=self.clear_chat)
        file_menu.add_command(label="退出", command=self.root.quit)

        # 设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="设置", menu=settings_menu)
        settings_menu.add_command(label="Token 设置", command=self.show_token_settings)
        settings_menu.add_command(label="关于", command=self.show_about)

        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Token 状态显示
        self.token_status = tk.StringVar(value="Token: 未设置")
        token_label = ttk.Label(main_frame, textvariable=self.token_status, foreground="red")
        token_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # 对话显示区域
        chat_frame = ttk.LabelFrame(main_frame, text="对话历史", padding="5")
        chat_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=70,
            height=25,
            state='disabled',
            font=('Microsoft YaHei UI', 10)
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置文本标签颜色
        self.chat_display.tag_config('user', foreground='#0066cc', font=('Microsoft YaHei UI', 10, 'bold'))
        self.chat_display.tag_config('assistant', foreground='#009900', font=('Microsoft YaHei UI', 10))

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.message_input = ttk.Entry(input_frame, width=80, font=('Microsoft YaHei UI', 10))
        self.message_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.message_input.bind('<Return>', lambda event: self.send_message())

        send_button = ttk.Button(input_frame, text="发送", command=self.send_message)
        send_button.grid(row=0, column=1)

        input_frame.columnconfigure(0, weight=1)

        # 更新 Token 状态
        self.update_token_status()

    def update_token_status(self):
        """更新 Token 状态显示"""
        if self.token:
            self.token_status.set(f"Token: 已设置 ({self.token[:10]}...)")
            self.message_input.config(state='normal')
        else:
            self.token_status.set("Token: 未设置")
            self.message_input.config(state='disabled')

    def display_chat_history(self):
        """显示对话历史"""
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)

        for msg in self.chat_history:
            role = msg.get('role', '')
            content = msg.get('content', '')

            if role == 'user':
                self.chat_display.insert(tk.END, f"\n您: {content}\n", 'user')
            elif role == 'assistant':
                self.chat_display.insert(tk.END, f"\n助手: {content}\n", 'assistant')

        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def add_message(self, role, content):
        """添加消息到显示区域"""
        self.chat_display.config(state='normal')

        if role == 'user':
            self.chat_display.insert(tk.END, f"\n您: {content}\n", 'user')
        elif role == 'assistant':
            self.chat_display.insert(tk.END, f"\n助手: {content}\n", 'assistant')

        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send_message(self):
        """发送消息"""
        message = self.message_input.get().strip()

        if not message:
            return

        if not self.token:
            messagebox.showwarning("警告", "请先设置 API Token！")
            self.show_token_settings()
            return

        # 清空输入框
        self.message_input.delete(0, tk.END)
        self.message_input.config(state='disabled')

        # 添加用户消息到显示
        self.add_message('user', message)
        self.chat_history.append({'role': 'user', 'content': message})

        # 在新线程中发送请求
        threading.Thread(target=self._send_request, args=(message,), daemon=True).start()

    def _send_request(self, message):
        """发送 API 请求"""
        try:
            response_text = self.call_coze_api(self.token, message, self.device_id)

            # 添加助手回复到显示
            self.root.after(0, lambda: self.add_message('assistant', response_text))
            self.chat_history.append({'role': 'assistant', 'content': response_text})

            # 保存对话历史
            self.save_chat_history()

        except Exception as e:
            error_msg = f"错误: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))

        finally:
            # 恢复输入框
            self.root.after(0, lambda: self.message_input.config(state='normal'))

    def call_coze_api(self, token, message, session_id):
        """调用 Coze API"""
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'content': {
                'query': {
                    'prompt': [
                        {
                            'type': 'text',
                            'content': {
                                'text': message
                            }
                        }
                    ]
                }
            },
            'type': 'query',
            'session_id': session_id,
            'project_id': self.PROJECT_ID
        }

        response = requests.post(
            self.API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )

        if response.status_code != 200:
            if response.status_code == 401:
                raise Exception('API Token 无效')
            elif response.status_code == 429:
                raise Exception('请求过于频繁')
            else:
                raise Exception(f'HTTP 错误: {response.status_code}')

        # 读取 SSE 格式的响应
        full_response = ''

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()

                if line_str.startswith('data: '):
                    json_str = line_str[6:]

                    try:
                        data = json.loads(json_str)
                        if isinstance(data, dict) and 'content' in data:
                            content = data.get('content', {})
                            answer = content.get('answer')

                            if answer:
                                full_response += answer
                    except json.JSONDecodeError:
                        pass

        if not full_response:
            raise Exception('服务器未返回有效响应')

        return full_response

    def clear_chat(self):
        """清空对话"""
        if messagebox.askyesno("确认", "确定要清空对话历史吗？"):
            self.chat_history = []
            self.chat_display.config(state='normal')
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state='disabled')

            # 删除历史文件
            if os.path.exists(self.history_file):
                os.remove(self.history_file)

    def show_token_settings(self):
        """显示 Token 设置窗口"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Token 设置")
        dialog.geometry("500x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # 框架
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Token 输入
        ttk.Label(frame, text="API Token:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        token_entry = ttk.Entry(frame, width=50, show="*")
        token_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        token_entry.insert(0, self.token)

        frame.columnconfigure(1, weight=1)

        # 按钮
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        def save_token():
            new_token = token_entry.get().strip()
            if len(new_token) < 10:
                messagebox.showwarning("警告", "Token 长度不能少于 10 个字符")
                return

            self.token = new_token
            self.save_config()
            self.update_token_status()
            messagebox.showinfo("成功", "Token 保存成功！")
            dialog.destroy()

        ttk.Button(button_frame, text="保存", command=save_token).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)

    def show_about(self):
        """显示关于信息"""
        about_text = """多智能体编剧系统

版本: 1.0.0

这是一个基于 LangChain 和 Coze 的多智能体编剧系统，帮助您创建剧本项目、生成分集大纲、编写剧本正文。

功能特点：
- 智能对话
- 项目管理
- 剧本创作
- 对话历史保存

技术栈：
- LangChain
- Coze API
- Python Tkinter
        """

        messagebox.showinfo("关于", about_text)

def main():
    root = tk.Tk()
    app = ScriptWriterGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
