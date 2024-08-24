from flask import Blueprint, request, jsonify
from models.users_auth import validate_credentials, register_user, update_password


# 创建蓝图
user = Blueprint('user', __name__)

# # 驗證帳號和密碼 API
# @user.route('/validate', methods=['POST'])
# def validate():
#     data = request.get_json()
#     account = data.get('username')
#     password = data.get('password')

#     response, status_code = validate_credentials(account, password)
#     return jsonify(response), status_code



# 用戶注冊
@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    account = data.get('username')
    password = data.get('password')

    response, status_code = register_user(account, password)
    return jsonify(response), status_code
    
# 更新密碼
@user.route('/password', methods=['PUT'])
def updatePassword():
    data = request.get_json()
    account = data.get('username')
    new_password = data.get('new_password')

    response, status_code = update_password(account=account, new_password=new_password)
    return jsonify(response), status_code