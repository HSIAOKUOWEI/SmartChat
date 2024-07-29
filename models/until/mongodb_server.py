from pymongo import MongoClient
from ..config import mongodb_ip, mongodb_port, mg_db


def get_mongodb_db(ip: str = mongodb_ip, 
                   port:int = mongodb_port, 
                   db_name: str = mg_db, 
                   tb_name:str = "" ):
    
    client = MongoClient(f'mongodb://{mongodb_ip}:{port}/')

    # 沒指定表，就返回db
    if not tb_name:  
        db = client[db_name]
        return db
    # 指定表，就返回db.tb_name
    else:
        db = client[db_name]
        table = db[tb_name]
        return table


if __name__ == '__main__':
    db = get_mongodb_db()
    users_collection = db['users']
    user =users_collection.find_one({"account": "11"})
    print(user)
    print(user["_id"])
