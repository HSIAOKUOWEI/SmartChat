from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from ..until.mongodb_server import get_mongodb_db
from bson.objectid import ObjectId


# import os
# from dotenv import load_dotenv
# from ..config import env_path
# load_dotenv(dotenv_path=env_path)

class filesInput(BaseModel):
    query: str = Field(description="What does the user want to do with the file?") # 用戶想要對文件做什麼
    file_ids: str = Field(description="File ids, separated by commas") # 文件id


def file_retriver(query, file_ids):
    """Used to process files uploaded by users"""
    # """用來處理用戶上傳的文件"""
    document = ""
    return document

# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"File read failed: `{error.args[0]}`"


file_reader = StructuredTool.from_function(
    func=file_retriver,
    name="file_retriver",
    args_schema=filesInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)