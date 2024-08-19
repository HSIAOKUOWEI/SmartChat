from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from ..until.mongodb_server import get_mongodb_db
from bson.objectid import ObjectId
from ..rag_common.get_source_file import get_source_file

# import os


class filesInput(BaseModel):
    query: str = Field(description="The specific task or question to search for in the document") # 要在文件中搜尋的具體任務或者問題
    file_ids: str = Field(description="File ids, separated by commas") # 文件id


def file_retriver(query, file_ids):
    """Can search for content related to a specific question within uploaded files"""
    # """可以在上傳的文件中搜尋與特定問題相關的內容"""

    file_relevant_content= {}




    #  document{文件id: {"file_name": "", "file_type": "", "temp_file_path": ""} , ....}
    file_data = get_source_file(file_ids)
    for file_id, data in file_data.items():
        pass
    
    # 向量化階段
    # 1.讀取文件，講pdf轉成圖片，講

    # 2. 使用多模態依據每一張圖片，生成摘要，假設性問題，生成答案

    # 3.
    # 3.1 將圖片原始檔保存到mongdb，返回圖片索引給metadata索引
    # 3.2製作langchain document類型，metadata:{文件id，文件名，頁數，圖片原始索引}，保存到milvus向量資料庫


    # 檢索生成階段
    # 1.判斷query否是要重寫擴寫

    # 2.依據重寫擴寫後的query檢索(向量，BM25，KNN，SVM)向量資料庫

    # 3.rerank排序，然後再去重取前N個
    
    # 3.提取相關的原始文件： 根據檢索出來的文件提取metadata裡面原始文件索引
    
    # 4.根據原始相關文件，生成相關原始文件摘要

    # 5.return : {文件id:{文件名:""，原始問題:""，檢索相關結果摘要:""}, }


    file_relevant_content[file_id] = {
        "file_name": data["file_name"], 
        "query": query,
        "relevant_content_summary": relevant_content_summary
    }

    return file_relevant_content

# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"File read failed: `{error.args[0]}`"


file_reader = StructuredTool.from_function(
    func=file_retriver,
    name="file_retriver",
    args_schema=filesInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)