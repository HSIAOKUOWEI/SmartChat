import re
from pymongo import errors
from bson import ObjectId
from .database.mongodb_server import get_mongodb_db
from datetime import datetime, timezone

# 連接MongoDB
db = get_mongodb_db(db_name='mydatabase')
users_collection = db['users']

# 驗證賬號和密碼合規性的正則表達式
account_regex = re.compile(r'^[a-zA-Z0-9_]+$')
password_regex = re.compile(r'^[a-zA-Z0-9_@#$%^&+=]+$')



# 驗證賬密是否合規
def validate_user(account, password):
    if not account or not password:
        return "Account and password are required"
    if not account_regex.match(account):
        return "Account contains invalid characters"
    if not password_regex.match(password):
        return "Password contains invalid characters"
    return None
# 檢查賬戶是否存在
def check_account_exists(account):
    if users_collection.find_one({"account": account}):
        return "Account already exists"
    return None
# 驗證登錄，成功則返回user_id
def validate_credentials(account, password):
    if not account or not password:
        return "Account and password are required"

    user = users_collection.find_one({"account": account})
    if user and user['password'] == password:
        # 更新最後登錄時間
        users_collection.update_one(
            {"account": account},
            {"$set": {"last_login": datetime.now(timezone.utc)}} #更新最後登錄時間
        )
        # ObjectId 类型不能直接序列化为 JSON。您需要将 ObjectId 转换为字符串格式
        return {"user_id": str(user['_id'])}, True
    else:
        return "Invalid account or password", 400
# 用戶註冊
def register_user(account, password):
    # 驗證用戶輸入
    validation_error = validate_user(account, password)
    if validation_error:
        return None, validation_error
    # 檢查帳號是否存在
    account_error = check_account_exists(account)
    if account_error:
        return None, account_error    
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
        return True, None
    except errors.DuplicateKeyError:
        return None, "User ID already exists"

# 更新密碼
def update_password(account, new_password):
    # 返回更新狀態，訊息
    validation_error = validate_user(account, new_password)
    if validation_error:
        return False, validation_error

    user = users_collection.find_one({"account": account})
    if not user:
        return False, "Account does not exist"    
    users_collection.update_one(
        {"account": account},
        {"$set": {"password": new_password, "password_last_modified": datetime.now(timezone.utc)}}
    )
    return True, "Password updated successfully"