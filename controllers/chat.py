from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models.jwt_utils import verify_token
chatbot_bp = Blueprint('chat', __name__)

# 模擬存儲聊天記錄
chat_history = []

@chatbot_bp.before_request
def check_token():
    if request.endpoint and 'static' in request.endpoint: 
        return
    token = request.cookies.get('token')
    if not token:
        print("Token not found, redirecting to login.")
        return redirect(url_for('auth.login'))

    user_id, payload = verify_token(token)
    if not user_id:
        print("Invalid or expired token, redirecting to login.")
        return redirect(url_for('auth.login'))

    print(f"Valid token: {token}")
    print(f"Payload: {payload}")
    
@chatbot_bp.route('/chat', methods=['GET', 'POST'])
def chatchat():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data['message']
        chat_history.append({'type': 'user', 'message': user_message})

        # 這裡模擬 API 請求，實際應該調用你的機器人 API
        bot_response = get_bot_response(user_message)
        chat_history.append({'type': 'bot', 'message': bot_response})

        return jsonify({'message': bot_response})

    return render_template('chat.html', messages=chat_history)

def get_bot_response(user_message):
    # 這裡模擬機器人的回答
    # 實際應該調用你的機器人 API 並返回結果
    return f"Bot response to: {user_message}"
