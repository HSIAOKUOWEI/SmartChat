from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper

from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field

class arxivInput(BaseModel):
    title: str = Field(description="The search query title, please use the English title search")
    # num: int = Field(default=3, description="The number of scientific articles you want to retrieve. Default is 3.")
    # length: int = Field(default=300, description="The maximum length of each scientific article. Default is 300.")
    

def get_arxiv_paper(title: str) -> str: # , num:int, length:int
    """A wrapper around Arxiv.org for searching and retrieving scientific articles in various fields."""


    arxiv_wrapper = ArxivAPIWrapper(top_k_results= 3, # 返回幾篇論文
                              ARXIV_MAX_QUERY_LENGTH= 300) #每篇最長多少字
    
    arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

    return arxiv.run(title)


# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"No relevant papers found: `{error.args[0]}`"


# arxiv論文搜索
arxiv = StructuredTool.from_function(
    func=get_arxiv_paper,
    name="arxiv",
    # description= "A wrapper around Arxiv.org for searching and retrieving scientific articles in various fields.""
    args_schema=arxivInput,
    # return_direct=True,
    # coroutine=function,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)