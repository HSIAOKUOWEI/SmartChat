from .internet_search import internet_search
from .wikipedia_search import wikipedia_search
from .weather_search import taiwan_weather
from .arxiv_paper import arxiv
from .url_reader import url
from .text2images import image_generation
from .image2text import image_reader
from .rag_fileSummarize import file_summarize

tools = [internet_search,  # 網絡搜索
         wikipedia_search,  # 維基百科
         taiwan_weather,arxiv,  # 全台天氣
         url, # 網頁讀取
         image_generation, # 圖片生成
         image_reader, # 讀取圖片
         file_summarize, # 文件摘要
         ] 