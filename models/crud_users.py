import re
from pymongo import errors
from bson import ObjectId
from .until.mongodb_server import get_mongodb_db
from datetime import datetime, timezone

# 连接MongoDB
db = get_mongodb_db(db_name='mydatabase')
users_collection = db['users']

# 验证账户和密码合規性的正則表達式
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
# 檢查賬戶是否存在
def check_account_exists(account):
    if users_collection.find_one({"account": account}):
        return {"error": "Account already exists"}, 400
    return None

# 驗證登錄，成功則返回user_id
def validate_credentials(account, password):
    if not account or not password:
        return {"success": False, "message": "Account and password are required"}, 400

    user = users_collection.find_one({"account": account})
    if user and user['password'] == password:
        # 更新最后登录时间
        users_collection.update_one(
            {"account": account},
            {"$set": {"last_login": datetime.now(timezone.utc)}} #更新最後登錄時間
        )
        # ObjectId 类型不能直接序列化为 JSON。您需要将 ObjectId 转换为字符串格式
        return {"success": True, "message": "Credentials are valid", "user_id": str(user['_id'])}, 200
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
    
    current_time = datetime.now(timezone.utc)
    
    try:
        users_collection.insert_one({
            "_id": ObjectId(), #唯一id
            "account": account, # 賬號
            "password": password,  # 密碼
            "created_at": current_time, # 創建時間
            "last_login": None, # 最後登錄時間
            "password_last_modified": current_time # 密碼上次修改時間
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
    
    users_collection.update_one(
        {"account": account},
        {"$set": {"password": new_password, "password_last_modified": datetime.now(timezone.utc)}}
    )
    return {"success": True, "message": "Password updated successfully"}, 200