import os
from dotenv import load_dotenv
# 加载 .env 文件中的环境变量
env_path = env_path = os.path.join(os.path.dirname(__file__), '.env')
print(env_path)
load_dotenv(dotenv_path=env_path)

