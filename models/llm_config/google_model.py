from langchain_google_genai import ChatGoogleGenerativeAI

def google_llm(model_name="gemini-1.5-pro", google_api_key=None, temperature=0.7):
    # gemini-1.5-pro , gemini-1.5-flash, gemini-1.0-pro
    google_llm = ChatGoogleGenerativeAI(google_api_key=google_api_key,
                                        model=model_name,
                                        temperature=temperature)
    return google_llm

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    env_path =r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
    load_dotenv(dotenv_path=env_path)

    # 獲取 API Key
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm = google_llm(google_api_key=google_api_key)
    print(llm.invoke("hello").content)
