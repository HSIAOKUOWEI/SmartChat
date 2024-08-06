import pymongo
import gridfs
from datetime import datetime, timezone
import bson
from .until.mongodb_server import get_mongodb_db

# MongoDB connection
db = get_mongodb_db()
fs = gridfs.GridFS(db)
user_image_collection = db["user_image"]
user_file_collection = db["user_file"]

def upload_file_logic(user_id, file):
    try:
        file_name = file.filename
        file_type = file.content_type
        file_size = file.content_length

        if not file_name or not file_type or file_size is None:
            raise ValueError("Invalid file data")

        # 将文件存储在 GridFS 中
        gridfs_id = fs.put(file, filename=file_name, content_type=file_type)

        # 在 user_file 集合中创建记录
        file_record = {
            "user_id": bson.ObjectId(user_id),
            "gridfs_id": gridfs_id,
            "created_at": datetime.now(timezone.utc),
            "file_name": file_name,
            "file_type": file_type,
            "file_size": file_size
        }
        file_id = user_file_collection.insert_one(file_record).inserted_id

        return {"file_id": str(file_id)}

    except Exception as e:
        raise e

def upload_image_logic(user_id, image):
    try:
        image_name = image.filename
        image_type = image.content_type
        image_size = image.content_length

        if not image_name or not image_type or image_size is None:
            raise ValueError("Invalid image data")

        # 将图片存储在 GridFS 中
        gridfs_id = fs.put(image, filename=image_name, content_type=image_type)

        # 在 user_image 集合中创建记录
        image_record = {
            "user_id": bson.ObjectId(user_id),
            "gridfs_id": gridfs_id,
            "created_at": datetime.now(timezone.utc),
            "image_name": image_name,
            "image_type": image_type,
            "image_size": image_size
        }
        image_id = user_image_collection.insert_one(image_record).inserted_id

        return {"image_id": str(image_id)}

    except Exception as e:
        raise e