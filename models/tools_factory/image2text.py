from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from typing import Literal
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
env_path = r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
load_dotenv(dotenv_path=env_path)

class imagesInput(BaseModel):
    image: str = Field(description="需要讀取的圖片的路徑或是id") # 圖片路徑

    

def get_image_description(prompt, number, width, height, qu): # , num:int, length:int
    """Generate images based on user descriptions"""
    # """根据用户的描述生成图片"""

    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template="Generate a detailed prompt to generate an image based on the following description: {image_desc}",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return  DallEAPIWrapper(n=number, size= f"{width}x{height}", quality).run(chain.run(prompt))





# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"Image reading failed: `{error.args[0]}`"



# 讀取圖像
image_reader = StructuredTool.from_function(
    func=get_image,
    name="image_reader",
    args_schema=imagesInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)