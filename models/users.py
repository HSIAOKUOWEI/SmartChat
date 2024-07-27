import re
from pymongo import errors
from bson import ObjectId
from models.until.mongodb_server import get_mongodb_db

# 连接MongoDB
db = get_mongodb_db(db_name='mydatabase')
users_collection = db['users']

# 验证账户和密码的正则表达式
account_regex = re.compile(r'^[a-zA-Z0-9_]+$')
password_regex = re.compile(r'^[a-zA-Z0-9_@#$%^&+=]+$')

# 驗證賬密是否合規
def validate_user(account, password):
    if not account or not password:
        return {"error": "Account and password are required"}, 400

    if not account_regex.match(account):
        return {"error": "Account contains invalid characters"}, 400

    if not password_regex.match(password):
        return {"error": "Password contains invalid characters"}, 400

    return None
# 檢查賬戶是否存在
def check_account_exists(account):
    if users_collection.find_one({"account": account}):
        return {"error": "Account already exists"}, 400
    return None

# 
def validate_credentials(account, password):
    if not account or not password:
        return {"success": False, "message": "Account and password are required"}, 400

    user = users_collection.find_one({"account": account})
    if user and user['password'] == password:
        return {"success": True, "message": "Credentials are valid"}, 200
    else:
        return {"success": False, "message": "Invalid account or password"}, 401

# 用戶註冊
def register_user(account, password):
    validation_error = validate_user(account, password)
    if validation_error:
        return validation_error

    account_error = check_account_exists(account)
    if account_error:
        return account_error

    try:
        users_collection.insert_one({
            "_id": ObjectId(),
            "account": account,
            "password": password  # 直接存储密码
        })
        return {"success": True, "message": "User created successfully"}, 200
    except errors.DuplicateKeyError:
        return {"error": "User ID already exists"}, 400

# 更新密碼
def update_password(account, new_password):
    validation_error = validate_user(account, new_password)
    if validation_error:
        return validation_error

    user = users_collection.find_one({"account": account})
    if not user:
        return {"error": "Account does not exist"}, 404

    users_collection.update_one({"account": account}, {"$set": {"password": new_password}})
    return {"success": True, "message": "Password updated successfully"}, 200