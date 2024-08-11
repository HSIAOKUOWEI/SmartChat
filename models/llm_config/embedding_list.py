from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
import os

def load_openai_embeddings(api_key=None, model="text-embedding-ada-002"):
    # 加载环境变量
    env_path = r"D:\LLM_application\llm_flask\.env"  # 请改成自己的env文件路径
    load_dotenv(dotenv_path=env_path)
    
    return OpenAIEmbeddings(
        api_key= api_key or os.getenv("OPENAI_API_KEY"),
        model=model
    )

def load_huggingface_embeddings(
        cache_folder=None,
        model_name="BAAI/bge-large-en",
        device="cpu", # or cuda
        normalize_embeddings=True # or Flase
        ):
    
    # 使用用户传入的值，若未传入则使用默认值
    cache_folder = cache_folder or "default_path"
    
    return HuggingFaceBgeEmbeddings(
        cache_folder=cache_folder,
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={'normalize_embeddings': normalize_embeddings}
    )