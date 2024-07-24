from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from models.user import User
from models.jwt_utils import generate_token, verify_token, delete_token

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
                return redirect(url_for('agent_chat.agent_chat')) #url_for(藍圖名稱.藍圖下函數名稱)：返回函數名稱的路徑 

            return render_template('login.html')
        
        elif request.method == 'POST':
            data = request.json
            username = data.get('username')
            password = data.get('password')
            user = User.check_credentials(username = username, password = password)

            # 登錄成功，生成token
            if user["success"]:
                token = generate_token(user_id = user["user_name"])
                if token["success"]:
                    response = jsonify({"success": True, 
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
        delete = delete_token(token)
        if delete["success"]:
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
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error occurred",
            "data": {},
            "error": str(e)
        }), 500