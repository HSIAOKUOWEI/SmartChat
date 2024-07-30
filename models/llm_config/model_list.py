from collections import OrderedDict
# 模型列表
MODEL_LIST_DETAILS = OrderedDict([
    ("Openai", OrderedDict([
        ("gpt-4o-mini", "gpt-4o-mini"),
        ("gpt-4o", "gpt-4o")
    ])),
    ("Google", OrderedDict([
        ("Gemini 1.5 Pro", "gemini-1.5-pro"),
        ("Gemini 1.5 Flash", "gemini-1.5-flash"),
        ("Gemini 1.0 Pro", "gemini-1.0-pro")
    ])),
    ("Groq", OrderedDict([
        ("LLaMA3 8b", "llama3-8b-8192"),
        ("LLaMA3.1 8b", "llama-3.1-8b-instant"),
        ("LLaMA3 70b", "llama3-70b-8192"),
        ("LLaMA3.1 70b", "llama-3.1-70b-versatile"),
        ("LLaMa3 Groq 8b Tool Use", "llama3-groq-8b-8192-tool-use-preview"),
        ("LLaMA3 Groq 70b Tool Use", "llama3-groq-70b-8192-tool-use-preview"),
        ("Mixtral 8x7b", "mixtral-8x7b-32768"),
        ("Gemma 7b", "gemma-7b-it"),
        ("Gemma2 9b", "gemma2-9b-it")
    ]))
])


def get_model(model_type, model_name, api_key, temperature=0.7):
    if model_type == "Openai":
        from langchain_openai import ChatOpenAI
        # gpt-4o, gpt-4o-mini
        openai_llm = ChatOpenAI(api_key=api_key, model=model_name,temperature=temperature)
        return openai_llm
    
    elif model_type == "Google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        google_llm = ChatGoogleGenerativeAI(google_api_key=api_key,
                                            model=model_name,
                                        temperature=temperature)
        return google_llm
    
    elif model_type == "Groq":
        from langchain_groq import ChatGroq
        groq_llm = ChatGroq(groq_api_key=api_key,
                            model=model_name,
                            temperature=temperature)
        return groq_llm
    elif model_type == "Siliconflow":
        from langchain_openai import ChatOpenAI
        base_url = "https://api.siliconflow.cn/v1"
        siliconflow_llm = ChatOpenAI(api_key=api_key, 
                                model=model_name,
                                temperature=temperature,
                                base_url=base_url)
        return siliconflow_llm
    

