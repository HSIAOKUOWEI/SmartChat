from flask import Blueprint, request, jsonify
import pymongo
from models.crud_history import get_user_id # 獲取user_id
import gridfs
from datetime import datetime, timezone
import bson
from models.upload_file import upload_file_logic, upload_image_logic


file_bp = Blueprint('file', __name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
fs = gridfs.GridFS(db)
user_image_collection = db["user_image"] # 保存文件
user_file_collection = db["user_file"] # 保存圖片

@file_bp.route('/file/upload', methods=['POST'])
def upload_file():
    try:
        token = request.cookies.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 400

        user_id = get_user_id(token)
        if not user_id:
            return jsonify({"error": "Invalid user"}), 401

        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        result = upload_file_logic(user_id, file)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_bp.route('/image/upload', methods=['POST'])
def upload_image():
    try:
        token = request.cookies.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 400

        user_id = get_user_id(token)
        if not user_id:
            return jsonify({"error": "Invalid user"}), 401

        image = request.files.get('image')
        if not image:
            return jsonify({"error": "No image uploaded"}), 400

        result = upload_image_logic(user_id, image)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
