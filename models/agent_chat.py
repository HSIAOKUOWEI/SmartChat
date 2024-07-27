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
llm = get_model(model_type="Openai", model_name="gpt-4o-mini", api_key=openai_api_key)

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools) # ,verbose=True
# print(agent_executor.invoke({"input": "宜蘭和金門的天氣如何"}))

# for chunk in agent_executor.stream({"input": "先寫一個排序算法,然後再幫我查一下台南跟金門的天氣,然後再維基百科查一下2024年台灣總統是誰"}):
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

# import pprint

# chunks = []

# for chunk in agent_executor.stream(
#     {"input": "先寫一個排序算法,然後再幫我查一下台南跟金門的天氣,然後再維基百科查一下2024年台灣總統是誰，再搜一下今年奧運會再在哪裡主辦"}
# ):
#     chunks.append(chunk)
#     print("------")
#     print(chunk)

# print("chuncks: ", chunks)