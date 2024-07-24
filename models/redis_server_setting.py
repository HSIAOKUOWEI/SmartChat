import redis
from .envLoad import REDIS_HOST, REDIS_PORT, REDIS_DB


redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

model_list = {
    "Openai":{"gpt-4o":"gpt-4o",
            "gpt-4o-mini":"gpt-4o-mini"},

    "Google":{"Gemini 1.5 Pro":"gemini-1.5-pro",
            "Gemini 1.5 Flash":"gemini-1.5-flash",
            "Gemini 1.0 Pro":"gemini-1.0-pro"},

    "Groq":{"LLaMA3 8b":"llama3-8b-8192" , 
            "LLaMA3 70b":"llama3-70b-8192",
            "LLaMa3 Groq 8b Tool Use": "llama3-groq-8b-8192-tool-use-preview",
            "LLaMA3 Groq 70b Tool Use":"llama3-groq-70b-8192-tool-use-preview" ,
            "Mixtral 8x7b": "mixtral-8x7b-32768",
            "Gemma 7b": "gemma-7b-it" , 
            "Gemma2 9b": "gemma2-9b-it"}
              }
