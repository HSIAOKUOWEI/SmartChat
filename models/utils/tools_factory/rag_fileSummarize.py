
from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.parsers.pdf import PyPDFParser

from ...model_list import get_model
from ..rag_common.get_source_file import get_source_file
import os

class fileInput(BaseModel):
    file_ids: str = Field(description="File ids, separated by commas") # 圖片id




def get_file_summary(file_ids):
    """Used to generate summaries or overviews of files uploaded by users, including extracting key information and creating concise summaries"""
    # """用來產生使用者上傳文件的摘要或概述，包括提取關鍵資訊和建立簡短總結"""
    
    # return: 字典，包含檔案ID、檔案名丶類型、內容(臨時檔案的路徑)
    file_data = get_source_file(file_ids)
    # 使用PyPDFLoader解析PDF文件
    parser = PyPDFParser()
    # langchain Document的列表
    # print(documents)
    print(file_data)
    # 初始化返回结果
    summary_data = {}

    for file_id, data in file_data.items():
        try:
            # 處理PDF檔案
            if data["file_type"] == "application/pdf" and data["documents_stream"]:
                from langchain_community.document_loaders import PyPDFLoader
                llm = get_model()
                documents = parser.parse(data["documents_stream"])
                chain = load_summarize_chain(llm, chain_type="stuff")
                result = chain.invoke(documents)
                summary = result["output_text"]
                    
        finally:
            # 删除临时文件
            # os.remove(path)
            pass


        # 保存{文件id:{文件名, 文件摘要}}
        summary_data[file_id] = {
            "file_name": data["file_name"],
            "summary": summary
        }
    
    return summary_data

# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"File summary generation failed: `{error.args[0]}`"


file_summarize = StructuredTool.from_function(
    func=get_file_summary,
    name="file_summarize",
    args_schema=fileInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)