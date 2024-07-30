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
    model: Literal["dall-e-3", "dall-e-2"] = Field(default="dall-e-2", description="When you need high quality, please choose 'dall-e-3'") # 使用的模型
    prompt: str = Field(description="User description of the image") # 用戶對於圖片的描述  
    number: int = Field(default=1, description="The number of images to be generated") #　需生成图片的数量
    width: Literal[256, 512, 1024] = Field(default=512, description="The width of the generated image") # 生成图片的宽度
    height: Literal[256, 512, 1024] = Field(default=512, description="The height of the generated image") # 生成图片的高度
    quality: Literal["standard", "hd"] = Field(default="strandard", description="The quality of the generated image") # 圖片的質量

    

def get_image(model, prompt, number, width, height, quality): # , num:int, length:int
    """Generate images based on user descriptions"""
    # """根据用户的描述生成图片"""
    try:
        return  DallEAPIWrapper(model=model, 
                                n=number, 
                                size= f"{width}x{height}", 
                                quality=quality).run(prompt)
    except Exception as e:
        print(e)
        return "Image generation failed"


# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"Image generation failed: `{error.args[0]}`"


# 圖像生成
image_generation = StructuredTool.from_function(
    func=get_image,
    name="images_genetarion",
    args_schema=imagesInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)