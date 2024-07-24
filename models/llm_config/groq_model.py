from langchain_groq import ChatGroq

# llama3-8b-8192 , llama3-70b-8192
# llama3-groq-70b-8192-tool-use-preview , llama3-groq-8b-8192-tool-use-preview
# mixtral-8x7b-32768
# gemma-7b-it , gemma2-9b-it
# 
# whisper-large-v3
def groq_llm(model_name="llama3-70b-8192", groq_api_key=None, temperature=0.5):
    groq_llm = ChatGroq(groq_api_key=groq_api_key,
                        model="llama3-70b-8192",
                        temperature=temperature)
    return groq_llm

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    env_path =r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
    load_dotenv(dotenv_path=env_path)
    # groq_api_key = os.getenv("GROQ_API_KEY")



    from langchain.chat_models import init_chat_model

    llm = init_chat_model("gemini-1.5-pro", model_provider="google_genai", temperature=0)
    results =llm.invoke("寫一個排序算法")
    print(results.content)