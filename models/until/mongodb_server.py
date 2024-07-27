from pymongo import MongoClient
from pymongo.database import Database
from ..config import mongodb_ip, mongodb_port, mg_db


def get_mongodb_db(ip: str = mongodb_ip, port:int = mongodb_port, db_name: str = mg_db ) -> Database:
    
    client = MongoClient(f'mongodb://{mongodb_ip}:{port}/')
    db = client[db_name]
    return db
