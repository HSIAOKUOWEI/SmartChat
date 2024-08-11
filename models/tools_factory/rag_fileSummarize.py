from ..until.mongodb_server import get_mongodb_db
from bson.objectid import ObjectId
import gridfs


import os
from dotenv import load_dotenv
from ..config import env_path
load_dotenv(dotenv_path=env_path)

from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from ..llm_config.embedding_list import load_openai_embeddings
from langchain_openai import ChatOpenAI

class fileInput(BaseModel):
    file_ids: str = Field(description="File ids, separated by commas") # 圖片id


def save_to_temp_file(content, suffix):
    import tempfile
    """
        將位元組內容儲存到臨時檔案並返回檔案路徑
        :param content: 檔案的位元組內容
        :param suffix: 檔案的後綴（例如 '.pdf' 或 '.xlsx'）
        :return: 臨時檔案的路徑
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

def get_source_file(file_ids):
    """
        從GridFS取得文件原始檔案
        :param file_ids: 逗號分隔的檔案ID列表
        :return: 字典，包含檔案ID、類型、內容
    """
    # 設置mongodb連接
    db = get_mongodb_db()
    user_file_collection = db["user_file"]
    fs = gridfs.GridFS(db)
    
    # 根據file_ids得到的gridfs_id獲取原始檔案
    source_files = {}
    
    # 将file_ids字符串分割为列表
    file_id_list = file_ids.split(',')

    for file_id in file_id_list:
        # 通過文件id以獲取gridfs_id、文件名和文件類型
        file_record = user_file_collection.find_one({"_id": ObjectId(file_id.strip())})
        if file_record:
            gridfs_id = file_record.get("gridfs_id")
            file_name = file_record.get("file_name")  
            file_type = file_record.get("file_type")
            suffix = '.' + file_name.split('.')[-1]  # 获取文件的后缀

            if gridfs_id:
                # 从GridFS中獲取文件内容
                source_file = fs.get(ObjectId(gridfs_id)).read()

                # 将文件内容保存到临时文件，并获取文件路径
                temp_file_path = save_to_temp_file(source_file, suffix)
                
                
                source_files[file_id] = {
                    "file_name": file_name,
                    "file_type": file_type,
                    "temp_file_path": temp_file_path  # 返回临时文件路径
                }
            else:
                source_files[file_id] = {
                    "file_name": file_name,
                    "file_type": None,
                    "temp_file_path": None
                }
        else:
            source_files[file_id] = {
                "file_name": None,
                "file_type": None,
                "temp_file_path": None
            }
    
    return source_files

def get_file_summary(file_ids):
    """Used to generate summaries or overviews of files uploaded by users, including extracting key information and creating concise summaries"""
    # """用来生成用户上传文件的摘要或概述，包括提取关键信息和创建简短总结"""
    file_data = get_source_file(file_ids)
    # 初始化返回结果
    summary_data = {}

    for file_id, data in file_data.items():
        if data["file_type"] == "application/pdf" and data["temp_file_path"]:
            from langchain_community.document_loaders import PyPDFLoader
            pdf_path = data["temp_file_path"]
            try:
                # 使用文件路径处理文件
                loader = PyPDFLoader(pdf_path)
                docs = loader.load()
                # 处理PDF文档
            finally:
                # 删除临时文件
                os.remove(pdf_path)


        # 保存{文件id:{文件名, 文件摘要}}
        summary_data[file_id] = {
            "file_name": data["file_name"],
            "summary": "summary"
        }
    
    return summary_data

# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"File summary generation failed: `{error.args[0]}`"


image_reader = StructuredTool.from_function(
    func=get_file_summary,
    name="file_summarize",
    args_schema=fileInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)