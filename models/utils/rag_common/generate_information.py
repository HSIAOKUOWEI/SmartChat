from langchain_core.messages import HumanMessage
import asyncio

from ...model_list import get_model
from .rag_prompt import get_prompt



async def process_and_save_image(file_name, user_id, images_base64):
    llm = get_model()
    
    # 1.為每張圖片並發生成摘要、假設性回答、假設性問題
    # 2.保留原始資訊到mongodb中，格式化為Document類
    # 3.保存到向量庫
    tasks = [generate_info_and_save(llm, image_base64, file_name, user_id, page_number + 1)
             for page_number, image_base64 in enumerate(images_base64)]

    # 執行所有任務
    image_info_list = await asyncio.gather(*tasks)

    return image_info_list
        

async def generate_info_and_save(llm, image_base64, file_name, user_id, page_number):
    
    # 並發生成summary, question, answer
    print("page_number: ", page_number)
    summary_task = image_prompt_format(llm, image_base64, prompt_type="summary")
    question_task = image_prompt_format(llm, image_base64, prompt_type="question")
    answer_task = image_prompt_format(llm, image_base64, prompt_type="answer")

    # 等待所有任務完成
    summary, question, answer = await asyncio.gather(summary_task, question_task, answer_task)

    # 返回每張圖片的信息字典
    image_info_dict = {
        "user_id": user_id,
        "filename": file_name,
        "page_number": page_number,
        "imge_base64": image_base64,
        "summary": summary,
        "question": question,
        "answer": answer
    }
    return image_info_dict


async def image_prompt_format(llm, image_base64, prompt_type="summary"):
    # 指定圖片生成什麼類別的資訊，假設性回答、假設性問題、摘要
    system_prompt_type = get_prompt(prompt_type=prompt_type)

    prompt = [
        {"type": "text", "text": system_prompt_type},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
    ]
    # 異步調用 LLM 生成圖像信息
    image_info = await llm.ainvoke([HumanMessage(content=prompt)])
    return image_info.content
