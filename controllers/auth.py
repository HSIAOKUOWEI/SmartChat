from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from ..models.until.jwt_utils import generate_token, verify_token, delete_token
from ..models.crud_users import validate_credentials
# import logging
# # 配置日志记录
# logging.basicConfig(filename='./app.log',level=logging.INFO)

auth_bp = Blueprint('auth', __name__)

# 訪問根目錄直接推送到登錄路由
@auth_bp.route('/')
def root():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            # 检查jwt token是否已存在，如果存在就重定向到使用界面
            token = request.cookies.get('token')
            verify = verify_token(token)
            if verify["success"]:
                return redirect(url_for('chat.agent_chat')) #url_for(藍圖名稱.藍圖下函數名稱)：返回函數名稱的路徑 

            return render_template('login.html')
        
        elif request.method == 'POST':
            data = request.json
            username = data.get('username')
            password = data.get('password')

             # 调用验证账号和密码的函数
            validate_response, status_code = validate_credentials(username, password)

            # logging.info(f'Validation response: {validate_response}, status_code: {status_code}')

            # 登录成功，生成token
            if status_code == 200 and validate_response.get("success"):
                token = generate_token(user_name = username, user_id=validate_response.get("user_id"))
                # logging.info(f'Token generation response: {token}')

                if token["success"]:
                    response = jsonify({
                        "success": True,
                        "message": "Login successful",
                        "data": {}
                    })
                    response.set_cookie('token', token["token"], httponly=True, samesite='Strict')  # 将token存储在cookie中

                    return response, 200
                
            # 登錄失敗
            else:
                return jsonify({
                    "success": False,
                    "message": "Invalid username or password",
                    "data": {}
                }), 401
            
    # 服務器請求失敗 
    except Exception as e:
        # logging.error(f'Exception occurred: {str(e)}')

        return jsonify({
            "success": False,
            "message": "An error occurred",
            "data": {},
            "error": str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        token = request.cookies.get('token')
        message,status = delete_token(token)
        if status == 200:
            response = jsonify({
                "success": True,
                "message": "Logout successful",
                "data": {}
            })
            response.delete_cookie('token')
            return response, 200
        else:
            return jsonify({
                "success": False,
                "message": "Invalid token",
                "data": {}
            }), 401
        
    # 服務器請求失敗 
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error occurred",
            "data": {},
            "error": str(e)
        }), 500