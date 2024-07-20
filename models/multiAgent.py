import os
from dotenv import load_dotenv
env_path =r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
load_dotenv(dotenv_path=env_path)
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OOPENAI_API_KEY")


from llm_config.google_model import google_llm
from llm_config.openai_model import openai_llm
from tools_factory.all_tools import tools
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

# llm = google_llm(google_api_key=google_api_key)
llm = openai_llm(api_key=openai_api_key)
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools) # ,verbose=True
# print(agent_executor.invoke({"input": "宜蘭和金門的天氣如何"}))

for chunk in agent_executor.stream({"input": "宜蘭和金門的天氣如何"}):
    if "actions" in chunk:
        for action in chunk["actions"]:
            print(f"Calling Tool: `{action.tool}` with input `{action.tool_input}`")
    # Observation
    elif "steps" in chunk:
        for step in chunk["steps"]:
            print(f"Tool Result: `{step.observation}`")
    # Final result
    elif "output" in chunk:
        print(f'Final Output: {chunk["output"]}')
    else:
        raise ValueError()
    print("---")

