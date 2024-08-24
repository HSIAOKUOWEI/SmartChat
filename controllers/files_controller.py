from flask import Blueprint, request, jsonify

from models.dialogue import get_user_id # 獲取user_id
from models.files import upload_file_logic, upload_image_logic
from models.utils.rag_common.make_embedding_vectordb import embedding_document
import asyncio


files = Blueprint('files', __name__)

@files.route('/documents', methods=['POST'])
async def upload_file():
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

        file_content = file.read()
        file_name = file.filename

        # 并行執行兩個函數，生成embedding並保存原始文件和embedding
        save_file_task = asyncio.to_thread(upload_file_logic, user_id, file) #將同步包裝成異步
        embedding_file_task = embedding_document(file_name, file_content, user_id) #異步函數

        file_id, _ = await asyncio.gather(save_file_task, embedding_file_task)
        return jsonify(file_id), 201

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@files.route('/image', methods=['POST'])
async def upload_image():
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

        result = await asyncio.to_thread(upload_image_logic,user_id, image)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
