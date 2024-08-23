import asyncio
from .convert_file import convert_pdf_to_images
from .generate_information import process_and_save_image
from ...database.milvus_server import get_milvus_db
from .make_ducuments import format_info_and_save
import time



async def embedding_document(file_name, file_content, user_id):
    try:
        # start =time.time()

        # 將pdf轉成圖片,返回所有圖片的base64
        images_base64 = await convert_pdf_to_images(file_content)

        # 生成圖片生成相關摘要 & 假設性回答 & 假設性問題
        image_info_list = await process_and_save_image(file_name, user_id, images_base64)

        # 先保留原始資訊到mongodb中，格式化後再保存到向量資料庫
        documents = await format_info_and_save(image_info_list)

        # documents保存到向量数据库
        get_milvus_db(docs=documents)

        # print(time.time()-start)
    
    except Exception as e:
        raise e