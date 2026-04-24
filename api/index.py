from flask import Flask, request, jsonify, Response
import os
import json

app = Flask(__name__)

# API 配置
API_URL = 'https://2km4yszdhf.coze.site/stream_run'
PROJECT_ID = 7632132891593703478

# 存储文件路径
TOKEN_FILE = '/tmp/tokens.json'
CHATS_FILE = '/tmp/chats.json'

# 确保数据目录存在
os.makedirs('/tmp', exist_ok=True)

def load_tokens():
    """加载所有 Token"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_tokens(tokens):
    """保存所有 Token"""
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)

def load_chats():
    """加载所有对话"""
    if os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_chats(chats):
    """保存所有对话"""
    with open(CHATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(chats, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """主页面"""
    try:
        html_file = os.path.join(os.path.dirname(__file__), '..', 'scriptwriter_cloud.html')
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading page: {str(e)}", 500

@app.route('/favicon.ico')
def favicon():
    """网站图标"""
    gif_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
    return Response(gif_data, mimetype='image/gif')

@app.route('/settings')
def settings():
    """设置页面"""
    try:
        html_file = os.path.join(os.path.dirname(__file__), '..', 'scriptwriter_settings.html')
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading settings page: {str(e)}", 500

@app.route('/token-config')
def token_config():
    """Token 配置工具（临时）"""
    try:
        html_file = os.path.join(os.path.dirname(__file__), '..', 'token-config.html')
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading token-config: {str(e)}", 500

@app.route('/diagnostic')
def diagnostic():
    """诊断工具"""
    try:
        html_file = os.path.join(os.path.dirname(__file__), '..', 'diagnostic.html')
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading diagnostic: {str(e)}", 500

@app.route('/test')
def test_page():
    """测试页面"""
    try:
        html_file = os.path.join(os.path.dirname(__file__), '..', 'test.html')
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading test page: {str(e)}", 500

@app.route('/api/token', methods=['GET', 'POST'])
def api_token():
    """Token API"""
    if request.method == 'POST':
        data = request.json
        device_id = data.get('device_id')
        token = data.get('token')

        if device_id and token:
            tokens = load_tokens()
            tokens[device_id] = token
            save_tokens(tokens)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': '缺少参数'}), 400
    else:
        # GET
        device_id = request.args.get('device_id')
        if device_id:
            tokens = load_tokens()
            token = tokens.get(device_id, '')
            return jsonify({'token': token, 'has_token': bool(token)})
        else:
            return jsonify({'success': False, 'error': '缺少 device_id'}), 400

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """聊天 API"""
    data = request.json
    device_id = data.get('device_id')
    message = data.get('message')
    token = data.get('token')

    if not device_id or not message:
        return jsonify({'success': False, 'error': '缺少参数'}), 400

    # 如果没有传入 token，尝试从存储中获取
    if not token:
        tokens = load_tokens()
        token = tokens.get(device_id, '')

    if not token:
        return jsonify({'success': False, 'error': '未设置 Token'}), 401

    try:
        response_text = call_coze_api(token, message, device_id)

        # 保存对话历史
        chats = load_chats()
        if device_id not in chats:
            chats[device_id] = []

        chats[device_id].append({
            'role': 'user',
            'content': message,
            'timestamp': str(int(os.time() * 1000))
        })

        chats[device_id].append({
            'role': 'assistant',
            'content': response_text,
            'timestamp': str(int(os.time() * 1000))
        })

        # 保留最近 100 条消息
        if len(chats[device_id]) > 100:
            chats[device_id] = chats[device_id][-100:]

        save_chats(chats)

        return jsonify({
            'success': True,
            'response': response_text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chats', methods=['GET', 'DELETE'])
def api_chats():
    """对话历史 API"""
    device_id = request.args.get('device_id')

    if not device_id:
        return jsonify({'success': False, 'error': '缺少 device_id'}), 400

    chats = load_chats()

    if request.method == 'DELETE':
        # 清空对话历史
        if device_id in chats:
            del chats[device_id]
            save_chats(chats)
        return jsonify({'success': True})
    else:
        # 获取对话历史
        return jsonify({
            'success': True,
            'chats': chats.get(device_id, [])
        })

def call_coze_api(token, message, session_id):
    """调用 Coze API"""
    import requests

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
        'project_id': PROJECT_ID
    }

    response = requests.post(
        API_URL,
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

# Vercel Serverless Function entry point
def handler(event, context):
    """Vercel Serverless Function handler"""
    return app(event, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
