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