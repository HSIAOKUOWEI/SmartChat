from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from models.utils.jwt_utils import generate_token, verify_token, delete_token
from models.users_auth import validate_credentials
from .utils.response_formatter import ApiResponse
# import logging
# 設定日誌記錄
# logging.basicConfig(filename='./app.log',level=logging.INFO)

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            # 檢查jwt token是否已存在，如果存在就重定向到使用介面
            token = request.cookies.get('token')
            verify = verify_token(token)
            if verify["success"]:
                return redirect(url_for('chat.agent_chat')) #url_for(藍圖名稱.藍圖下函數名稱)：返回函數名稱的路徑 

            return render_template('login.html')
        
        elif request.method == 'POST':
            data = request.json
            username = data.get('username')
            password = data.get('password')

             # 驗證帳號和密碼
            validate_response, status_code = validate_credentials(username, password)

            # logging.info(f'Validation response: {validate_response}, status_code: {status_code}')

            # 登入成功，產生token
            if status_code:
                token = generate_token(user_name = username, user_id=validate_response["user_id"])
                # logging.info(f'Token generation response: {token}')

                if token["success"]:
                    response = ApiResponse.success(message="Login successful")
                    response[0].set_cookie('token', token["token"], httponly=True, samesite='Strict')  # 将token存储在cookie中

                    return response
                
            # 登錄失敗
            else:

                return ApiResponse.error(message="Invalid username or password", status_code=401)

            
    # 服務器請求失敗 
    except Exception as e:
        return ApiResponse.error(message="INTERNAL_ERROR", status_code=500)


@auth.route('/logout', methods=['POST'])
def logout():
    try:
        token = request.cookies.get('token')
        message,status = delete_token(token)
        if status == 200:
            response = ApiResponse.success(message="Logout successful")
            response[0].delete_cookie('token')
            return response
        else:
            return ApiResponse.error(message="Invalid token", status_code=401)
        
    # 服務器請求失敗 
    except Exception as e:
        return ApiResponse.error(message="INTERNAL_ERROR", status_code=500)