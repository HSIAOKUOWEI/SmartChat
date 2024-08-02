import os
from dotenv import load_dotenv
env_path =r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
load_dotenv(dotenv_path=env_path)
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

from .llm_config.model_list import get_model
from .tools_factory.all_tools import tools
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)


# llm = get_model(model_type="Google", model_name="gemini-1.5-pro", api_key=google_api_key)
# llm = get_model(model_type="Groq", model_name="llama3-groq-70b-8192-tool-use-preview", api_key=groq_api_key)
# llm = get_model(model_type="Groq", model_name="llama-3.1-70b-versatile", api_key=groq_api_key)

llm = get_model(model_type="Openai", model_name="gpt-4o-mini", api_key=openai_api_key)

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools) # ,verbose=True
# print(agent_executor.invoke({"input": "宜蘭和金門的天氣如何"}))
# input = "幫我查一下台北天氣"
# for chunk in agent_executor.stream({"input": input}):
#     if "actions" in chunk:
#         for action in chunk["actions"]:
#             print(f"Calling Tool: `{action.tool}` with input `{action.tool_input}`")
#     # Observation
#     elif "steps" in chunk:
#         for step in chunk["steps"]:
#             print(f"Tool Result: `{step.observation}`") #api的結果
#     # Final result
#     elif "output" in chunk:
#         print(f'Final Output: {chunk["output"]}')
#     else:
#         raise ValueError()
#     print("---")

# on_chat_model_stream 是模型最終的輸出
# async def generate_response(input):
#     async for event in agent_executor.astream_events({"input": input}, version="v1"):
#         if event["event"] == "on_chain_end":
#             print(event)
            # if event["event"] == "on_chat_model_stream":
            #      continue
            #     # print(event["data"]["chunck"].content) # chunk一定會有的, 因為有on_chat_model_stream就會有chunk
                 
            # #     content = event["data"]["chunk"].content
            # #     if content:
            # #         # yield content
            # #         print(content)
            # elif event["event"] == "on_tool_start":
            #     # 開始執行工具
            #     # print(event)
            #     # event['name'] 調用工具的名稱 'name': 'taiwai_weather'
            #     # event["data"]["input"] 工具的輸入 'data': {'input': {'city': '臺南市'}}
            #     # event["data"].get("input") 用get取值，有些工具不需要輸入參數，get就返回None
            #     print(event['name'],": ",event["data"].get("input"))
                
            # elif event["event"] == "on_tool_end":
            #     # 工具輸入結束後的回傳結果
            #     # print(event)
            #     # event['name'] 調用工具的名稱 'name': 'taiwai_weather'
            #     # event['ouput'] 工具的輸出
            #     print( event['name'],": ", event['data'].get('output'))
            # else:
            #      print(event)

# import asyncio
# asyncio.run(generate_response(input=input))