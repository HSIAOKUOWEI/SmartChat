from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field

from bson.objectid import ObjectId
from ..rag_common.rewrite_query import rewrite


# import os


class filesInput(BaseModel):
    query: str = Field(description="User questions") # 用戶的問題
    file_ids: str = Field(description="File ids, separated by commas") # 文件id


def file_retriver(query, file_ids):
    """Can search for content related to a specific question within uploaded files"""
    # """用來搜尋用戶上傳文件中的内容"""

    file_relevant_content= {}

    # 1.判斷query否是要重寫擴寫，返回list of questions
    questions = rewrite(question=query)

    # 2.依據重寫擴寫後的query檢索(向量，BM25，KNN，SVM)向量資料庫
    # 3.rerank排序，然後再去重取前N個
    # 4.提取前N個相關的原始文件： 原始文件中的metadata裡面有原始文件索引
    # 5.根據原始相關文件，生成相關原始文件摘要
    # 6.return : {文件id:{文件名:""，原始問題:""，檢索相關結果摘要:""}, }
    for question in questions:
        for file_id in file_ids.split(","):

            # 先從mongodb user_file中獲取user_id

            # Milvus使用user_id和file_id過濾匹配

            # 取出ducoment中所有page_content重排序，返回前N個

            # 依據前N個ducoments中的file_id和page_number取出關聯的原始圖片

            # 輸入：documents的原始圖片和原始用戶問題

            # 函數一：input:(question,file_id) output:relevant_content
            break

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