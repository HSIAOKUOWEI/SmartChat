from flask import Blueprint, render_template, request, jsonify, redirect, url_for, Response
from models.jwt_utils import verify_token
from models.llm_config.google_model import google_llm


agentChat_bp = Blueprint('agent_chat', __name__)

# 模擬存儲聊天記錄
chat_history = []

@agentChat_bp.before_request
def check_token():
    # 如果请求的 endpoint 包含 'static'，则直接返回
    if request.endpoint and 'static' in request.endpoint: 
        return

    # 从请求中获取 'token' 的 cookie 值
    token = request.cookies.get('token')
    # 驗證 token
    verify = verify_token(token)

    # 驗證失敗，重定向到登录页面
    if not verify["success"]:
        print("Invalid or expired token, redirecting to login.")
        return redirect(url_for('auth.login'))

@agentChat_bp.route('/agent_chat', methods=['GET', 'POST'])
def agent_chat():
    if request.method == 'POST':
        # 打印接收到的FormData数据
        print("Received FormData:")
        for key, value in request.form.items():
            print(f"{key}: {value}")

        # 提取文字消息
        message = request.form.get('message')
        
        # 提取文件和图片
        files = request.files.getlist('files')
        images = request.form.getlist('images')

        # 打印接收到的数据
        print("Received message:", message)
        print("Received files:", [file.filename for file in files])
        print("Received images:", images)

        # 保存到聊天记录
        chat_history.append({'type': 'user', 'message': message, 'files': [file.filename for file in files], 'images': images})

        # 模拟机器人的响应
        llm = google_llm(google_api_key="AIzaSyBraz_OmCCH7LW8ffESP0pItKjdtCTKMJQ")
        # bot_response = llm.invoke(message)

        # bot_response = get_bot_response(message)
        # chat_history.append({'type': 'bot', 'message': bot_response.content})
        # return jsonify({
        #     'success': True,
        #     'message': 'Data received successfully',
        #     'data': {
        #         'text': bot_response.content,
        #     }
        # })
        def generate_response(message):
            for chunk in llm.stream(message):
                yield chunk.content

        return Response(generate_response(message=message), mimetype='text/event-stream')
    
        # return jsonify({
        #     'success': True,
        #     'message': 'Data received successfully',
        #     'data': {
        #         'text': message,
        #         'files': [file.filename for file in files],
        #         'images': images
        #     }
        # })

    return render_template('chat.html', messages=chat_history)

def get_bot_response(user_message):
    # 这里模拟机器人的回答
    # 实际应该调用你的机器人 API 并返回结果
    return f"Bot response to: {user_message}"
