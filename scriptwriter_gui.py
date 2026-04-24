#!/usr/bin/env python3
"""
多智能体编剧系统 - 图形界面版本
带项目历史管理和知识库功能
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import requests
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional

# 配置
API_URL = 'https://2km4yszdhf.coze.site/stream_run'
PROJECT_ID = 7632132891593703478

# 本地存储文件
DATA_FILE = 'scriptwriter_gui_data.json'


class ScriptwriterGUI:
    """编剧系统图形界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎭 多智能体编剧系统")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        # 状态
        self.api_token = ''
        self.session_id = ''
        self.connected = False
        self.is_sending = False
        self.current_project = None

        # 本地数据
        self.projects = {}  # {project_id: {name, description, history: []}}
        self.chat_history = []  # [{role, content, timestamp}]

        # 加载本地数据
        self.load_data()

        # 创建界面
        self.create_widgets()

        # 检查 Token
        if self.api_token:
            self.connect_to_agent()

    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # 左侧边栏（项目列表）
        sidebar = ttk.Frame(main_container, width=250, relief="ridge", padding="5")
        sidebar.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        main_container.columnconfigure(0, weight=0)

        # 标题
        title_label = ttk.Label(sidebar, text="📁 项目列表", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))

        # 项目列表
        self.project_listbox = tk.Listbox(sidebar, height=20)
        self.project_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.project_listbox.bind('<<ListboxSelect>>', self.on_project_select)
        self.refresh_project_list()

        # 操作按钮
        button_frame = ttk.Frame(sidebar)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="➕ 新建项目", command=self.new_project).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="🔄 刷新列表", command=self.refresh_project_list).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="⚙️ 设置 Token", command=self.set_token).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="🔍 联网搜索", command=self.web_search_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="💾 导出对话", command=self.export_chat).pack(fill=tk.X, pady=2)

        # 右侧主区域
        main_frame = ttk.Frame(main_container)
        main_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_container.columnconfigure(1, weight=1)

        # 连接状态栏
        self.status_label = ttk.Label(main_frame, text="⚫ 未连接", relief="sunken")
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        main_frame.rowconfigure(0, weight=0)
        main_frame.columnconfigure(0, weight=1)

        # 聊天区域
        chat_frame = ttk.Frame(main_frame)
        chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(1, weight=1)

        # 消息显示区
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Microsoft YaHei UI", 10),
            state='disabled'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.tag_config("user", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="green", font=("Arial", 10))
        self.chat_display.tag_config("system", foreground="gray", font=("Arial", 9, "italic"))
        self.chat_display.tag_config("error", foreground="red", font=("Arial", 10))

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        main_frame.rowconfigure(2, weight=0)
        main_frame.columnconfigure(0, weight=1)

        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=4,
            wrap=tk.WORD,
            font=("Microsoft YaHei UI", 10)
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())
        self.input_text.bind('<Shift-Return>', lambda e: None)

        # 发送按钮
        send_frame = ttk.Frame(input_frame)
        send_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Button(send_frame, text="发送 (Ctrl+Enter)", command=self.send_message).pack(side=tk.RIGHT)
        ttk.Button(send_frame, text="清空对话", command=self.clear_chat).pack(side=tk.RIGHT, padx=(0, 5))

    def load_data(self):
        """加载本地数据"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.api_token = data.get('api_token', '')
                    self.projects = data.get('projects', {})
                    self.chat_history = data.get('chat_history', [])
        except Exception as e:
            print(f"加载数据失败: {e}")

    def save_data(self):
        """保存本地数据"""
        try:
            data = {
                'api_token': self.api_token,
                'projects': self.projects,
                'chat_history': self.chat_history
            }
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def refresh_project_list(self):
        """刷新项目列表"""
        self.project_listbox.delete(0, tk.END)

        if not self.projects:
            self.project_listbox.insert(tk.END, "📭 暂无项目")
            return

        for project_id, project in self.projects.items():
            display_text = f"📄 {project.get('name', '未命名')}"
            self.project_listbox.insert(tk.END, display_text)

    def on_project_select(self, event):
        """选择项目"""
        selection = self.project_listbox.curselection()
        if selection:
            index = selection[0]
            if self.projects:
                project_ids = list(self.projects.keys())
                if index < len(project_ids):
                    project_id = project_ids[index]
                    self.load_project_chat(project_id)

    def new_project(self):
        """新建项目"""
        dialog = tk.Toplevel(self.root)
        dialog.title("新建项目")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="项目名称：").pack(pady=10)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5)

        ttk.Label(dialog, text="项目类型：").pack(pady=5)
        type_combo = ttk.Combobox(dialog, values=["电影", "电视剧", "网剧", "短视频", "话剧", "动画"], state="readonly")
        type_combo.set("电视剧")
        type_combo.pack(pady=5)

        ttk.Label(dialog, text="项目描述：").pack(pady=5)
        desc_text = scrolledtext.ScrolledText(dialog, height=6, width=40)
        desc_text.pack(pady=5)

        def create():
            name = name_entry.get().strip()
            project_type = type_combo.get()
            description = desc_text.get("1.0", tk.END).strip()

            if not name:
                messagebox.showerror("错误", "请输入项目名称")
                return

            import uuid
            project_id = str(uuid.uuid4())
            self.projects[project_id] = {
                'name': name,
                'type': project_type,
                'description': description,
                'created_at': datetime.now().isoformat(),
                'history': []
            }

            self.current_project = project_id
            self.chat_history = []
            self.save_data()
            self.refresh_project_list()
            self.clear_chat()
            dialog.destroy()

            self.add_message("system", f"✅ 已创建项目：{name}")

        ttk.Button(dialog, text="创建", command=create).pack(pady=10)

    def load_project_chat(self, project_id):
        """加载项目对话"""
        if project_id not in self.projects:
            return

        self.current_project = project_id
        project = self.projects[project_id]
        self.chat_history = project.get('history', [])
        self.save_data()

        self.clear_chat()
        for msg in self.chat_history:
            self.add_message(msg['role'], msg['content'], display_only=True)

    def set_token(self):
        """设置 API Token"""
        dialog = tk.Toplevel(self.root)
        dialog.title("设置 API Token")
        dialog.geometry("500x200")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="API Token：", font=("Arial", 10, "bold")).pack(pady=10)
        token_entry = ttk.Entry(dialog, width=50, show="*")
        token_entry.pack(pady=5)
        token_entry.insert(0, self.api_token)

        # 显示/隐藏密码
        def toggle_password():
            if token_entry.cget('show') == '*':
                token_entry.config(show='')
            else:
                token_entry.config(show='*')

        ttk.Button(dialog, text="显示/隐藏", command=toggle_password).pack(pady=5)

        ttk.Label(dialog, text="在 Coze 平台获取：https://coze.com/user/pat", foreground="blue", cursor="hand2").pack(pady=5)

        def save():
            token = token_entry.get().strip()
            if not token.startswith('pat_'):
                messagebox.showwarning("警告", "Token 应该以 'pat_' 开头")
                return

            self.api_token = token
            self.save_data()
            dialog.destroy()
            self.connect_to_agent()

        ttk.Button(dialog, text="保存", command=save).pack(pady=10)

    def connect_to_agent(self):
        """连接到智能体"""
        if not self.api_token:
            self.status_label.config(text="⚫ 未设置 Token")
            return

        import random
        import string
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
        self.session_id = f"gui_session_{int(time.time())}_{random_str}"

        self.status_label.config(text="🔄 正在连接...")

        try:
            # 发送测试消息
            response = self.send_to_api("你好", is_test=True)
            if response:
                self.connected = True
                self.status_label.config(text="🟢 已连接")
                self.add_message("assistant", f"✅ 连接成功！\n\n{response}")
            else:
                self.status_label.config(text="🔴 连接失败")
                self.add_message("error", "❌ 连接失败：未收到响应")
        except Exception as e:
            self.connected = False
            self.status_label.config(text="🔴 连接失败")
            self.add_message("error", f"❌ 连接失败：{str(e)}")

    def send_to_api(self, text, is_test=False):
        """发送消息到 API"""
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
                timeout=300
            )

            if response.status_code != 200:
                if response.status_code == 401:
                    raise Exception("API Token 无效")
                elif response.status_code == 429:
                    raise Exception("请求过于频繁")
                else:
                    raise Exception(f"HTTP 错误: {response.status_code}")

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

            return full_response if full_response else None

        except requests.exceptions.Timeout:
            raise Exception("请求超时")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接错误")
        except Exception as e:
            raise e

    def send_message(self):
        """发送消息"""
        if self.is_sending:
            return

        text = self.input_text.get("1.0", tk.END).strip()

        if not text:
            return

        if not self.connected:
            messagebox.showerror("错误", "请先设置 Token 并连接")
            return

        self.is_sending = True
        self.status_label.config(text="🔄 正在发送...")
        self.root.update()

        # 显示用户消息
        self.add_message("user", text)
        self.input_text.delete("1.0", tk.END)

        # 发送到 API
        try:
            response = self.send_to_api(text)
            if response:
                self.add_message("assistant", response)
            else:
                self.add_message("error", "❌ 未收到响应")
        except Exception as e:
            self.add_message("error", f"❌ 发送失败：{str(e)}")
        finally:
            self.is_sending = False
            self.status_label.config(text="🟢 已连接" if self.connected else "🔴 未连接")

    def add_message(self, role, content, display_only=False):
        """添加消息到聊天区域"""
        self.chat_display.config(state='normal')

        # 添加时间戳
        timestamp = datetime.now().strftime("%H:%M:%S")
        role_names = {
            "user": "👤 你",
            "assistant": "🤖 智能体",
            "system": "ℹ️ 系统",
            "error": "❌ 错误"
        }

        self.chat_display.insert(tk.END, f"\n[{timestamp}] {role_names.get(role, role)}\n", role)
        self.chat_display.insert(tk.END, content + "\n\n")

        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

        # 保存到历史
        if not display_only:
            self.chat_history.append({
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat()
            })

            # 如果有当前项目，保存到项目历史
            if self.current_project and self.current_project in self.projects:
                self.projects[self.current_project]['history'] = self.chat_history

            self.save_data()

    def clear_chat(self):
        """清空对话"""
        self.chat_display.config(state='normal')
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state='disabled')

    def export_chat(self):
        """导出对话"""
        if not self.chat_history:
            messagebox.showinfo("提示", "暂无对话历史")
            return

        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile=f"对话记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for msg in self.chat_history:
                        role = msg['role']
                        content = msg['content']
                        timestamp = msg['timestamp']

                        f.write(f"[{timestamp}] {role}\n")
                        f.write(f"{content}\n\n")

                messagebox.showinfo("成功", f"对话已导出到：{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败：{str(e)}")

    def web_search_dialog(self):
        """联网搜索对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("联网搜索")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="搜索内容：", font=("Arial", 10, "bold")).pack(pady=10)
        search_entry = ttk.Entry(dialog, width=50)
        search_entry.pack(pady=5)

        ttk.Label(dialog, text="功能：", font=("Arial", 10, "bold")).pack(pady=5)
        desc_label = ttk.Label(dialog, text="联网搜索 → AI分析类型 → 自动分类 → 保存到知识库", foreground="gray")
        desc_label.pack(pady=5)

        result_text = scrolledtext.ScrolledText(dialog, height=15, width=60, state='disabled')
        result_text.pack(pady=10, padx=10)

        def do_search():
            query = search_entry.get().strip()
            if not query:
                messagebox.showerror("错误", "请输入搜索内容")
                return

            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"🔍 正在搜索：{query}\n\n", "system")
            result_text.config(state='disabled')
            dialog.update()

            try:
                # 调用智能体进行搜索
                message = f"请使用联网搜索功能搜索：{query}，并自动分类保存到知识库"
                response = self.send_to_api(message)

                if response:
                    result_text.config(state='normal')
                    result_text.insert(tk.END, f"✅ 搜索完成！\n\n{response}")
                    result_text.config(state='disabled')

                    # 也添加到主聊天
                    self.add_message("system", f"🔍 已搜索并保存：{query}")
                else:
                    result_text.config(state='normal')
                    result_text.insert(tk.END, "❌ 搜索失败：未收到响应", "error")
                    result_text.config(state='disabled')
            except Exception as e:
                result_text.config(state='normal')
                result_text.insert(tk.END, f"❌ 搜索失败：{str(e)}", "error")
                result_text.config(state='disabled')

        ttk.Button(dialog, text="🔍 开始搜索", command=do_search).pack(pady=10)


def main():
    """主函数"""
    root = tk.Tk()

    # 设置主题
    style = ttk.Style()
    style.theme_use('clam')

    app = ScriptwriterGUI(root)

    root.mainloop()


if __name__ == '__main__':
    main()
