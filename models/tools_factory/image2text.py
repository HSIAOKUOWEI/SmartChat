from langchain_core.tools import StructuredTool,ToolException
from langchain.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from ..until.mongodb_server import get_mongodb_db
from bson.objectid import ObjectId
import gridfs
import base64

import os
from dotenv import load_dotenv
env_path = r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
load_dotenv(dotenv_path=env_path)

class imagesInput(BaseModel):
    prompt: str = Field(description="What does the user want to do with the image?") # 用戶想要對圖片做什麼
    image_ids: str = Field(description="Image ids, separated by commas") # 圖片id


def get_base64_image_from_mongodb(image_ids):
    """
    从GridFS中获取图片及其类型，并转换为base64编码。

    :param image_ids: 逗号分隔的图片ID列表
    :return: 包含base64编码的图片和图片类型的字典列表
    """
    # 設置mongodb連接
    db = get_mongodb_db()
    user_iamge_collection = db["user_image"]
    fs = gridfs.GridFS(db)
    
    # 獲取image_id對應的圖片並轉換為base64编码
    base64_images = []
    for image_id in image_ids.split(","):
        image_data = user_iamge_collection.find_one({"_id": ObjectId(image_id)})
        if image_data:
            gridfs_id = image_data['gridfs_id']
            image_type = image_data.get('image_type', 'image/png')  # 默认为 'image/png'
            gridfs_file = fs.get(ObjectId(gridfs_id))
            base64_image = base64.b64encode(gridfs_file.read()).decode('utf-8')
            base64_images.append({
                "base64_image": base64_image,
                "image_type": image_type
            })
    return base64_images

def get_image_description(prompt, image_ids):
    """Used to process images uploaded by users"""
    # """用來處理用戶上傳的圖片"""

    # 獲取image_id對應的圖片並轉換為base64编码
    base64_images = get_base64_image_from_mongodb(image_ids)

    # prompt 格式化
    messages = [{"type": "text", "text": prompt}]
    for image in base64_images:
        base64_image = image['base64_image']
        image_type = image['image_type']
        messages.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{image_type};base64,{base64_image}"
            }
        })

    messages = HumanMessage(messages)
    llm =  ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))
    
    return llm.invoke([messages]).content

# 設置默認錯誤訊息
def _handle_error(error: ToolException) -> str:
    return f"Image reading failed: `{error.args[0]}`"


image_reader = StructuredTool.from_function(
    func=get_image_description,
    name="image_reader",
    args_schema=imagesInput,
    handle_tool_error=_handle_error, #用來提示工具錯誤，直接使用預設的錯誤提示，也可自訂
)