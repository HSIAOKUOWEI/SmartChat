import os
from dotenv import load_dotenv

env_path =r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
load_dotenv(dotenv_path=env_path)

# 獲取 API Key
google_api_key = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

REDIS_HOST = os.getenv("REDIS_HOST") # Redis服务器地址
REDIS_PORT = os.getenv("REDIS_PORT")  # Redis端口
REDIS_DB = os.getenv("REDIS_DB")  # Redis数据库编号
