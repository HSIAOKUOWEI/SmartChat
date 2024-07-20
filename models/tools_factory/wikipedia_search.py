from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from typing import Literal


class WikipediaInput(BaseModel):
    query: str = Field(description="The search query")
    # lang: Literal["en", "zh"] = Field(description="The language to search in", default="zh")

    

def wikipedia(query: str,) -> str:
    """ A wrapper that uses Wikipedia to search."""

    top_k_results: int = 3
    load_all_available_meta: bool = False
    doc_content_chars_max: int = 4000

    api_wrapper = WikipediaAPIWrapper(lang="zh",
        top_k_results=top_k_results,
        load_all_available_meta=load_all_available_meta,
        doc_content_chars_max=doc_content_chars_max,
    )

    wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper)

    return wikipedia.run(query) # type：str

# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"


# 维基百科搜索
wikipedia_search = StructuredTool.from_function(
    func=wikipedia,
    name="Wikipedia",
    description="A wrapper that uses Wikipedia to search.",
    args_schema=WikipediaInput,
    # return_direct=True,
    # coroutine=function,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)

# # type :str
# print(type(wikipedia_search.invoke({"query": "台北"})))
# print(wikipedia_search.invoke({"query": "台北"}))
