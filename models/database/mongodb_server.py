from pymongo import MongoClient
import os

# 从环境变量中获取 MongoDB 的 IP、端口和数据库名称
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongodb_ip = os.getenv('MONGO_IP')
mongodb_port = int(os.getenv('MONGO_PORT'))
mg_db = os.getenv('MONGO_DEFAULT_DB')
mongo_timeout = int(os.getenv('MONGO_TIMEOUT'))  # 连接超时，单位为毫秒

def get_mongodb_db(username: str = mongo_username, 
                   password: str = mongo_password,
                   ip: str = mongodb_ip, 
                   port: int = mongodb_port, 
                   db_name: str = mg_db, 
                   tb_name: str = "",
                   timeout: int = mongo_timeout):
    try:
        # 嘗試連接 Docker 容器中的 MongoDB
        # 一開始用戶默認創建在admin資料庫中，所以需要指定authSource=admin
        client = MongoClient(f'mongodb://{username}:{password}@{ip}:{port}/?authSource=admin',
                             serverSelectionTimeoutMS=timeout)
        # 测试连接
        client.admin.command('ping')

    except Exception as e:
        # 回退到使用 localhost
        client = MongoClient(f'mongodb://{username}:{password}@localhost:{port}/?authSource=admin',
                             serverSelectionTimeoutMS=timeout)
        # 測試連接
        client.admin.command('ping')
    
    # 沒指定表，就回傳資料庫
    db = client[db_name]
    if not tb_name:
        return db
    # 指定表，就回傳表
    else:
        table = db[tb_name]
        return table


if __name__ == '__main__':
    db = get_mongodb_db()
    users_collection = db['users']
    user =users_collection.find_one({"account": "11"})
    print(user)
    print(user["_id"])
