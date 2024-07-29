import requests
import re
from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from typing import List, Literal
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate


class imagesInput(BaseModel):
    prompt: str = Field(description="User description of the image") # 用戶對於圖片的描述
    number: int = Field(1, description="The number of images to be generated") #　需生成图片的数量
    width: Literal[256, 512, 1024] = Field(512, description="The width of the generated image") # 生成图片的宽度
    height: Literal[256, 512, 1024] = Field(512, description="he height of the generated image") # 生成图片的高度
    

def get_image(prompt, number, width, height): # , num:int, length:int
    """Generate images based on user descriptions"""
    # """根据用户的描述生成图片"""

    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template="Generate a detailed prompt to generate an image based on the following description: {image_desc}",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return  DallEAPIWrapper(api_key="",n=number, size= f"{width}x{height}").run(chain.run(prompt))





# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"Image generation failed: `{error.args[0]}`"


# 圖像生成
generation_image = StructuredTool.from_function(
    func=get_image,
    name="genetarion_images",
    args_schema=imagesInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)