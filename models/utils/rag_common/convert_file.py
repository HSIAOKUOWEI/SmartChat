import asyncio
import fitz
import bson
import base64
from datetime import datetime, timezone
from ...database.mongodb_server import get_mongodb_db

# 初始化数据库和GridFS
async def init_async_db():
    db = await asyncio.to_thread(get_mongodb_db)
    return db



async def convert_pdf_to_images(file_content):
    # 打开 PDF 文件
    pdf_document = fitz.open(stream=file_content, filetype="pdf")

    # 創建轉換頁面任務
    conversion_tasks = [asyncio.to_thread(convert_page_to_image, pdf_document, page_number)
                        for page_number in range(len(pdf_document))]
    
    # 一次執行所有轉換頁面任務
    images = await asyncio.gather(*conversion_tasks)

    return images

def convert_page_to_image(pdf_document, page_number):
    page = pdf_document.load_page(page_number)  # 加载页面
    pix = page.get_pixmap()  # 获取页面的像素图
    image_bytes = pix.tobytes("png")  # 將圖片轉換為 PNG 格式的位元組流

    # 將影像位元組流轉換為 Base64 編碼
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return image_base64


async def save_image_to_mongodb(user_id, image):
    db = await init_async_db()

    # 儲存格式
    image_record = {
        "user_id": bson.ObjectId(user_id),
        "image_data": image,
        "created_at": datetime.now(timezone.utc)
    }

    # 保存到 MongoDB 中的 user_image 集合
    result = await asyncio.to_thread(db.user_image.insert_one, image_record)
    return str(result.inserted_id)
