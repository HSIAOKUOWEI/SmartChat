import requests
import re
from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field

class urlInput(BaseModel):
    url: str = Field(description="The search query title, please use the English title search")
    # num: int = Field(default=3, description="The number of scientific articles you want to retrieve. Default is 3.")
    # length: int = Field(default=300, description="The maximum length of each scientific article. Default is 300.")
    

def get_url_content(url: str) -> str: # , num:int, length:int
    """Use this tool to get the clear content of a URL."""

    # 提取url文本中的网页链接部分。url文本可能是一句话
    url_pattern = r'http[s]?://[a-zA-Z0-9./?&=_%#-]+'
    match = re.search(url_pattern, url)
    url = match.group(0) if match else None

    if url is None:
        return "No url found in the input"
    
    
    # Jina AI Reader API
    reader_url = f"https://r.jina.ai/{url}"

    response = requests.get(reader_url) # , timeout=5
    if response.status_code == 200:
        result = {"result": response.text, 
                 "docs": [
                     {"page_content": response.text, 
                      "metadata": {'source': url, 'id': ''}}]}
        
        return result



# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"NO url : `{error.args[0]}`"


# 讀取網頁
url = StructuredTool.from_function(
    func=get_url_content,
    name="url",
    args_schema=urlInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)