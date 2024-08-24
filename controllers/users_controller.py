from flask import Blueprint, request, jsonify
from models.users_auth import validate_credentials, register_user, update_password
from .utils.response_formatter import ApiResponse

# 创建蓝图
users = Blueprint('users', __name__)

# # 驗證帳號和密碼 API
# @user.route('/validate', methods=['POST'])
# def validate():
#     data = request.get_json()
#     account = data.get('username')
#     password = data.get('password')

#     response, status_code = validate_credentials(account, password)
#     return jsonify(response), status_code



# 用户注册
@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    account = data.get('username')
    password = data.get('password')

    success, error_message = register_user(account, password)
    if error_message:
        return ApiResponse.error(message=error_message, status_code=400)
    
    return ApiResponse.success(message="User created successfully", status_code=201)

# 更新密码
@users.route('/password', methods=['PUT'])
def password():
    data = request.get_json()
    account = data.get('username')
    new_password = data.get('new_password')

    status, message = update_password(account=account, new_password=new_password)
    if status:
        return ApiResponse.success(message=message, status_code=200)
    
    return ApiResponse.error(message=message, status_code=400)

