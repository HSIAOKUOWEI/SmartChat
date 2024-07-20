from typing import Optional, Type

from langchain.pydantic_v1 import BaseModel
from langchain_core.callbacks import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

# 步驟1：定義tool的輸入
class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

# 步驟2：描述tool
class CustomCalculatorTool(BaseTool):
    name = "Calculator" # 給agent調用的名字
    description = "useful for when you need to answer questions about math" #教LLM什麼情況使用這個tool
    args_schema: Type[BaseModel] = CalculatorInput # 工具輸入為什麼
    return_direct: bool = True # True，则工具的结果直接返回。False，则可能需要通过某种机制（如回调函数）来获取结果

    def _run(
        self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return a * b

    async def _arun(
        self,
        a: int,
        b: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        # If the calculation is cheap, you can just delegate to the sync implementation
        # as shown below.
        # If the sync calculation is expensive, you should delete the entire _arun method.
        # LangChain will automatically provide a better implementation that will
        # kick off the task in a thread to make sure it doesn't block other async code.
        return self._run(a, b, run_manager=run_manager.get_sync())
    
multiply = CustomCalculatorTool()
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)

print(multiply.invoke({"a": 2, "b": 3}))
print((await multiply.ainvoke({"a": 2, "b": 3})))