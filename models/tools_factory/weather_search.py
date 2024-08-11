
from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
import requests

import os
from dotenv import load_dotenv
from ..config import env_path
load_dotenv(dotenv_path=env_path)

# 設定天氣API的授權碼
Authorization=os.getenv("opendataCWA_authorization")
# 指定LLM可以搜尋的城市格式
taiwan_citys = "宜蘭縣, 花蓮縣, 臺東縣, 澎湖縣, 金門縣, 連江縣, 臺北市, 新北市, 桃園市, 臺中市, 臺南市, 高雄市, 基隆市, 新竹縣, 新竹市, 苗栗縣, 彰化縣, 南投縣, 雲林縣, 嘉義縣, 嘉義市, 屏東縣"
class WeatherInput(BaseModel):
    city: str = Field(description=f"The cities in Taiwan, it must be one of following {taiwan_citys}")

    

def get_weather_data(city: str) -> str:
    """Get the weather for all cities in Taiwan"""
    # """可以獲取台灣所有城市的天氣"""

    # 天氣API
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={Authorization}&locationName={city}&elementName="
    response = requests.get(url)
    # 格式化資料
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"Failed to retrieve weather: `{error.args[0]}`"


# 獲取台灣城市天氣數據
taiwan_weather = StructuredTool.from_function(
    func=get_weather_data,
    name="taiwai_weather",
    description="Get the weather data for Taiwan",
    args_schema=WeatherInput,
    # return_direct=True,
    # coroutine=function,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    env_path =r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
    load_dotenv(dotenv_path=env_path)

    # 天氣API
    token=os.getenv("GOOGLE_API_KEY")
    city = "宜蘭縣"
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={token}&locationName={city}&elementName="
    response = requests.get(url)
    # 格式化資料
    if response.status_code == 200:
        print(response.json()) 
    else:
        print(response.status_code)