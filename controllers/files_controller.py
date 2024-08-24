from flask import Blueprint, request, jsonify
from .utils.response_formatter import ApiResponse
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
            return ApiResponse.error(message="Token is missing", status_code=400)

        user_id = get_user_id(token)
        if not user_id:
            return ApiResponse.error(message="Invalid user", status_code=401)

        file = request.files.get('file')
        if not file:
            return ApiResponse.error(message="No file uploaded", status_code=400)

        file_content = file.read()
        file_name = file.filename

        # 并行執行兩個函數，生成embedding並保存原始文件和embedding
        save_file_task = asyncio.to_thread(upload_file_logic, user_id, file) #將同步包裝成異步
        embedding_file_task = embedding_document(file_name, file_content, user_id) #異步函數

        file_id, _ = await asyncio.gather(save_file_task, embedding_file_task)
        return ApiResponse.success(data={"file_id": file_id}, status_code=201)

    except Exception as e:
        # print(e)
        return ApiResponse.error(message=str(e), status_code=500)

@files.route('/image', methods=['POST'])
async def upload_image():
    try:
        token = request.cookies.get('token')
        if not token:
            return ApiResponse.error(message="Token is missing", status_code=400)

        user_id = get_user_id(token)
        if not user_id:
            return ApiResponse.error(message="Invalid user", status_code=401)

        image = request.files.get('image')
        if not image:
            return ApiResponse.error(message="No image uploaded", status_code=400)

        image_id = await asyncio.to_thread(upload_image_logic,user_id, image)
        return ApiResponse.success(data={"image_id": image_id}, status_code=201)

    except Exception as e:
        return ApiResponse.error(message=str(e), status_code=500)
