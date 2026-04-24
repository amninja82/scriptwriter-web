#!/usr/bin/env python3
"""
多智能体编剧系统 - 本地代理服务器
解决 CORS 跨域问题
"""

from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

# 配置
API_URL = 'https://2km4yszdhf.coze.site/stream_run'
PROJECT_ID = 7632132891593703478

@app.route('/')
def index():
    """主页"""
    return '''
    <h1>多智能体编剧系统 - 代理服务器</h1>
    <p>代理服务器正在运行</p>
    <p>请使用 scriptwriter_chat_with_proxy.html 文件连接</p>
    '''

@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    """代理聊天请求"""
    try:
        # 获取请求数据
        data = request.json
        api_token = data.get('token')
        message_text = data.get('message')
        session_id = data.get('session_id', 'default_session')

        if not api_token:
            return jsonify({'error': '缺少 API Token'}), 400

        if not message_text:
            return jsonify({'error': '缺少消息内容'}), 400

        # 构建请求头和请求体
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'content': {
                'query': {
                    'prompt': [
                        {
                            'type': 'text',
                            'content': {
                                'text': message_text
                            }
                        }
                    ]
                }
            },
            'type': 'query',
            'session_id': session_id,
            'project_id': PROJECT_ID
        }

        # 发送请求到真实 API
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                'error': f'API 错误: {response.status_code}',
                'message': response.text
            }), response.status_code

        # 流式返回响应
        def generate():
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        yield json.dumps(data) + '\n'
                    except json.JSONDecodeError:
                        pass

        return Response(
            generate(),
            mimetype='application/json',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': '网络请求错误',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': '服务器错误',
            'message': str(e)
        }), 500

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': '代理服务器运行正常'})

if __name__ == '__main__':
    print("=" * 50)
    print("多智能体编剧系统 - 代理服务器")
    print("=" * 50)
    print(f"API 地址: {API_URL}")
    print(f"项目 ID: {PROJECT_ID}")
    print("=" * 50)
    print("启动中...")
    print("✅ 代理服务器已启动！")
    print("📡 监听地址: http://localhost:5000")
    print("🌐 请使用 scriptwriter_chat_with_proxy.html 连接")
    print("=" * 50)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
