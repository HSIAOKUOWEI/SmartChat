from flask import Blueprint, render_template, request, Response
from models.llm_config.model_list import get_model
import json
from models.agent_chat import agent_executor
from models.crud_history import save_message,get_user_id
from models.llm_config.agentChat_prompt import initialize_prompt
import asyncio


chat_bp = Blueprint('chat', __name__)
class StreamWithHeaders(Response):
    def __init__(self, response, headers=None, **kwargs):
        super().__init__(response, **kwargs)
        if headers:
            for header, value in headers.items():
                self.headers[header] = value

@chat_bp.route('/agent_chat', methods=['GET', 'POST'])
def agent_chat():
    if request.method == 'POST':
        # 提取token解析user_id
        token = request.cookies.get('token')
        user_id = get_user_id(token)

        history = json.loads(request.form.get('history'))  # 假设 history 是以 JSON 字符串形式传递的
        message = request.form.get('message') # 當前輸入
        model_type = request.form.get('model_type') # 模型類型
        model_name = request.form.get('model_name') # 模型名稱
        api_key = request.form.get('api_key') # api key
        dialogue_id = request.form.get('dialogue_id') # 當前對話框id
        
        # 处理上传的文件和图片 ID 以及文件名
        image_ids = request.form.getlist('image_ids')  # 获取所有 image_ids
        file_ids = request.form.getlist('file_ids')  # 获取所有 file_ids

        # 解析每一个 JSON 字符串并格式化为字典
        images = [json.loads(img) for img in image_ids]
        files = [json.loads(file) for file in file_ids]

        # 打印接收到的数据
        print("Received model_type:", model_type)
        print("Received model_name:", model_name)
        print("Received api_key:", api_key)
        print("Received dialogue_id:", dialogue_id)
        print("Received history:", history)
        print("Received message:", message)
        print("Received files:", files)
        print("Received images:", images)
        

        user_message_content = {"role": "user","content": message}

        dialogue_id = save_message(user_id, dialogue_id, user_message_content)
        headers = {"dialogue_id": dialogue_id} # 返回給前端

        prompt = initialize_prompt(chat_history = history,   # 聊天記錄
                                   user_message = message,   # 當前消息
                                   uploaded_files = files,   # 上傳文件
                                   uploaded_images = images, # 上傳的圖片
                                   prompt_language="ZH" #EN  # prompt版本
                                   ) 
        print(prompt)
        

        async def generate_response(input, userid, dialogueid):
            response = "" #用來保存輸出結果 
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
                    print(event)
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


            # 保存結果
            # # print(response)        
            bot_message_content = {"role": "assistant","content": response}
            save_message(user_id=userid, dialogue_id=dialogueid, message_content=bot_message_content)
            

        def generate_response_sync(input, userid, dialogueid):
            async_gen = generate_response(input=input, userid=userid, dialogueid=dialogueid)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                while True:
                    yield loop.run_until_complete(async_gen.__anext__())
            except StopAsyncIteration:
                pass
            finally:
                loop.close()
                
        return StreamWithHeaders(generate_response_sync(input=prompt, userid=user_id, dialogueid=dialogue_id), headers=headers, mimetype='text/event-stream')

        
        # return jsonify({
        #     'success': True,
        #     'message': 'Data received successfully',
        #     'data': {
        #         'text': message,
        #         'files': [file.filename for file in files],
        #         'images': images
        #     }
        # })

    return render_template('chat.html')

