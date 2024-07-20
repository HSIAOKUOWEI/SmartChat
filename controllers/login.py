from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from models.user import User
from models.jwt_utils import generate_token, verify_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def root():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # 检查jwt token是否已存在，如果存在就重定向到使用界面
        token = request.cookies.get('token')
        if token and verify_token(token):
            return redirect(url_for('chat.chatchat')) #url_for(藍圖名稱.藍圖下函數名稱)：返回函數名稱的路徑 
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.check_credentials(username = username, password = password)
        if user:
            token = generate_token(user_id = user.id, username = user.name)
            response = jsonify({"success": True, "message": "Login successful", "token": token})
            response.set_cookie('token', token)  # 将token存储在cookie中
            return response, 200
        else:
            return jsonify({"success": False, "message": "Invalid username or password"}), 401
