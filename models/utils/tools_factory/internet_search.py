from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
# 需更多附加資訊（例如連結、來源），請使用 DuckDuckGoSearchResults()
from langchain_community.tools import DuckDuckGoSearchResults,BingSearchResults
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
import re
import json
def format_text_to_list(text):
    # 正則表达式匹配每个列表項
    pattern = r'\[snippet: (.*?), title: (.*?), link: (.*?)\]'

    # 使用正則表達式尋找所有符合項
    matches = re.findall(pattern, text)

    # 创建结果列表
    result = []
    for match in matches:
        snippet, title, link = match
        result.append({
            "snippet": snippet.strip(),
            "title": title.strip(),
            "link": link.strip()
        })
    
    return result

# 設置工具錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"


# 定義工具輸入
class SearchInput(BaseModel):
    query: str = Field(description="query for Internet search")

# 定義工具如何調用，以及結果輸出
def duckduck_search(query: str) -> str:
    """Use this tool to use search engine to search the internet and get information."""
    search = DuckDuckGoSearchResults()
    # 格式化原始資料为[{'snippet': 'Obama', 'title': 'Obama, Barack', 'link': 'https://en.wikipedia.org/wiki/Barack_Obama'}]
    # raise ToolException(f"Error: There is no query by the name of {query}.") #設置默認工具錯誤提示
    return format_text_to_list(search.run(query))

def bing_search(query: str):
    search = BingSearchResults(api_wrapper=BingSearchAPIWrapper(key="<KEY>"))

    return search.run(query)

def tavily_search(query: str):
    api_wrapper = TavilySearchAPIWrapper(tavily_api_key="<KEY>")
    search = TavilySearchResults(api_wrapper=api_wrapper)

    return search.run(query)

# 設置默認錯誤訊息
internet_search = StructuredTool.from_function(
    func=duckduck_search, # 函數
    name="search_duckduck", # 工具名稱
    description="Use this tool to use search engine to search the internet and get information.", #什么時候調用這個工具
    args_schema=SearchInput, # 工具的輸入
    # return_direct=True, #直接返回結果
    # coroutine=Asearch_duckduck, #異步函數
    handle_tool_error=_handle_error, #設置錯誤訊息。保證工具出錯之後還可以繼續執行
)


# # type :list
# print(type(search_internet.invoke({"query": "台北今天的天氣如何"}))) #
# print(search_internet.invoke({"query": "台北今天的天氣如何"})) #

# #轉為json格式的字符串
# print(json.dumps(search_internet.invoke({"query": "台北今天的天氣如何"}), ensure_ascii=False, indent=2)) #字典
# # type:str
# print(type(json.dumps(search_internet.invoke({"query": "台北今天的天氣如何"}), ensure_ascii=False, indent=2)))

    
