from langchain_openai import ChatOpenAI

def openai_llm(model_name="gpt-4o-mini",api_key=None, temperature=0.5):
    llm = ChatOpenAI(model=model_name, api_key=api_key,temperature=temperature)
    return llm


