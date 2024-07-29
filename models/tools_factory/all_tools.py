from .internet_search import internet_search
from .wikipedia_search import wikipedia_search
from .weather_search import taiwan_weather
from .arxiv_paper import arxiv
from .url_reader import url
from .text2images import generation_image

tools = [internet_search,  # 網絡搜索
         wikipedia_search,  # 維基百科
         taiwan_weather,arxiv,  # 全台天氣
         url,
         generation_image] # 網頁讀取