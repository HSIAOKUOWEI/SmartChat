from langchain_core.documents import Document
from ...database.mongodb_server import get_mongodb_db
import asyncio
import bson
import re


async def get_file_id(user_id, file_name):
    db = await asyncio.to_thread(get_mongodb_db)
    collection = db['user_file']
    
    # 轮询直到获取到 file_id
    while True:
        file_record = await asyncio.to_thread(
            collection.find_one, 
            {"user_id": bson.ObjectId(user_id), "file_name": file_name}
        )
        if file_record:
            return str(file_record['_id'])
        await asyncio.sleep(0.1)  # 间隔 100ms 重试
# 保存原始的 image_info 到 MongoDB
async def save_images_info(images_info_list,file_id):
    # 将 file_id 添加到每个 image_info 中
    for image_info in images_info_list:
        image_info['file_id'] = file_id

    db = await asyncio.to_thread(get_mongodb_db)
    collection = db['file_img']

    # 使用 insert_many 一次性插入所有 image_info 到 MongoDB
    await asyncio.to_thread(collection.insert_many, images_info_list)

# 格式化 Documents，返回生成的 Document 列表
async def format_images_info(images_info_list, file_id):
    documents = [] 

    # 定义正则表达式匹配编号 (1. 2. 3. ...)
    pattern = re.compile(r'\d+\.\s*')

    for image_info in images_info_list:
        # 为每一个 image_info 生成 Document 并添加到 documents 列表中
        summary_doc = Document(
            page_content=image_info["summary"],
            metadata={
                "user_id": image_info["user_id"],
                "file_id": file_id,
                "filename": image_info["filename"],
                "page_number": image_info["page_number"],
                "type": "summary",
            }
        )
        documents.append(summary_doc)

        # 使用正则表达式分割 question 并生成 Document
        question_parts = re.split(pattern, image_info["question"])
        for part in question_parts:
            if part.strip():  # 排除空白部分
                question_doc = Document(
                    page_content=part.strip(),
                    metadata={
                        "user_id": image_info["user_id"],
                        "file_id": file_id,
                        "filename": image_info["filename"],
                        "page_number": image_info["page_number"],
                        "type": "question",
                    }
                )
                documents.append(question_doc)

        # 使用正则表达式分割 answer 并生成 Document
        answer_parts = re.split(pattern, image_info["answer"])
        for part in answer_parts:
            if part.strip():  # 排除空白部分
                answer_doc = Document(
                    page_content=part.strip(),
                    metadata={
                        "user_id": image_info["user_id"],
                        "file_id": file_id,
                        "filename": image_info["filename"],
                        "page_number": image_info["page_number"],
                        "type": "answer",
                    }
                )
                documents.append(answer_doc)

        # 将生成的 Document 加入到返回的列表中
        documents.extend([summary_doc, question_doc, answer_doc])

    return documents

# 并行格式化并保存文件信息
async def format_info_and_save(images_info_list):
    # 获取原始文件file_id
    file_id = await get_file_id(images_info_list[0]["user_id"], images_info_list[0]["filename"])
    
    # 格式化為Documents類
    format_task = asyncio.create_task(format_images_info(images_info_list, file_id=file_id))
    # 為image_info增加file_id，然後保存至MongoDB
    save_task = asyncio.create_task(save_images_info(images_info_list, file_id=file_id))

    # 并行执行格式化和保存操作
    documents, _ = await asyncio.gather(format_task, save_task)
    
    return documents