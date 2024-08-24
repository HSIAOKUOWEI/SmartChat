from .model_list import get_model
from .utils.tools_factory.all_tools import tools
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import asyncio
import json
from .dialogue import save_message

# prompt定義
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# llm初始化
llm = get_model(model_type="Openai")

# agent初始化
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

# agent輸出處理
agent_executor = AgentExecutor(agent=agent, tools=tools) # ,verbose=True

# 用戶輸入初始化
def agent_prompt(chat_history, user_message, uploaded_files, uploaded_images, prompt_language="ZH"):
    if prompt_language == "ZH":
        prompt = f"""
請考慮以下信息以高效且有效地回應用戶的查詢。請考慮聊天記錄、用戶當前的話語以及任何上傳的文件或圖片。如果用戶的查詢與任何上傳的文件或圖片的內容相關，請分析並提供必要的信息，調用相應的工具。但是，如果用戶的查詢不需要上傳的文件或圖片，請優先直接回答他們的問題或使用其他相關工具。

### 聊天記錄
{chat_history}

### 用戶當前說的話
{user_message}

### 用戶上傳的檔案
{uploaded_files}

### 用戶上傳的圖片
{uploaded_images}

始終優先考慮用戶的當前查詢，只有在直接與用戶問題相關時才利用聊天記錄、文件或圖片。確保回應清晰、準確並有效滿足用戶需求。
                """
    else:  # Default to English
        prompt = f"""
please consider the following information to respond to the user's query efficiently and effectively. Take into account the chat history, the user's current message, and any uploaded files or images. If the user's query relates to the content of any uploaded files or images, analyze and provide the necessary information by invoking the appropriate tools. However, if the user's query does not require the uploaded files or images, prioritize answering their question directly or use other relevant tools.

### Chat History
{chat_history}

### User's Current Message
{user_message}

### Uploaded Files
{uploaded_files}

### Uploaded Images
{uploaded_images}

Always prioritize the user's current query and only utilize the chat history, files, or images if directly relevant to the user's question. Ensure the response is clear, accurate, and meets the user's needs effectively.
                """
    return prompt


async def agentChat_response(input, userid, dialogueid):
    response = "" #用來保存輸出結果 
    try:
        async for event in agent_executor.astream_events({"input": input}, version="v1"):
            # 加"\n"是因為yield不能保證每一次都是返回一條數據，
            # 所以用"\n"來區別每一次的數據
            if event["event"] == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                response += content
                if content:
                    #使用 jsonify會有問題，因為在返回的時候會把還未完成的異步任務給銷毀掉
                    yield json.dumps({
                                        "event": "on_chat_model_stream",
                                        "content": content
                                    })+ "\n"
            elif event["event"] == "on_tool_start":
                # print(event)
                yield json.dumps({
                                    "event": "on_tool_start",
                                    "name": event["name"],
                                    "inputs": event["data"].get("input")
                                })+ "\n"
                
            elif event["event"] == "on_tool_end":
                yield json.dumps({
                                    "event": "on_tool_end",
                                    "name": event["name"],
                                    "output": event["data"].get("output")
                                    })+ "\n"

    except Exception as e:
        # 如果有异常发生，打印出来，方便调试
        print(f"Error in agentChat_response: {str(e)}")
    finally:
        # 保存結果    
        bot_message_content = {"role": "assistant","content": response}
        save_message(user_id=userid, dialogue_id=dialogueid, message_content=bot_message_content)
    

def agentChat_response_sync(userid, dialogueid, history, message, files, images):
    prompt = agent_prompt(chat_history = history,   # 聊天記錄
                                   user_message = message,   # 當前消息
                                   uploaded_files = files,   # 上傳文件
                                   uploaded_images = images, # 上傳的圖片
                                   prompt_language="ZH" #EN  # prompt版本
                                   ) 
    
    # async for response in agentChat_response(input=prompt, userid=userid, dialogueid=dialogueid):
    #     yield response
    async_gen = agentChat_response(input=prompt, userid=userid, dialogueid=dialogueid)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        while True:
            yield loop.run_until_complete(async_gen.__anext__())
    except StopAsyncIteration:
        pass
    finally:
        loop.close()