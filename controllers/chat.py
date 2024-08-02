from flask import Blueprint, render_template, request, Response
from models.llm_config.model_list import get_model
import json
from models.agent_chat import agent_executor
from models.crud_history import save_message,get_user_id
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
        # 提取所有值
        token = request.cookies.get('token')
        user_id = get_user_id(token)

        history = json.loads(request.form.get('history'))  # 假设 history 是以 JSON 字符串形式传递的
        message = request.form.get('message')
        model_type = request.form.get('model_type')
        model_name = request.form.get('model_name')
        api_key = request.form.get('api_key')
        dialogue_id = request.form.get('dialogue_id')


        # 提取文件和图片
        files = request.files.getlist('files')
        images = request.form.getlist('images')

        # 打印接收到的数据
        print("Received history:", history)
        print("Received message:", message)
        print("Received model_type:", model_type)
        print("Received model_name:", model_name)
        print("Received api_key:", api_key)
        print("Received files:", [file.filename for file in files])
        print("Received images:", images)
        print("Received dialogue_id:", dialogue_id)

        user_message_content = {"role": "user","content": message}

        dialogue_id = save_message(user_id, dialogue_id, user_message_content)
        headers = {"dialogue_id": dialogue_id} # 返回給前端


        async def generate_response(input, userid=None, dialogueid=None):
            async for event in agent_executor.astream_events({"input": input}, version="v1"):
                if event["event"] == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield json.dumps({
                                            "event": "chat_content",
                                            "content": content
                                        })
                elif event["event"] == "on_tool_start":
                    yield json.dumps({
                                        "event": "start_tool",
                                        "name": event["name"],
                                        "inputs": event["data"].get("input")
                                    })
                elif event["event"] == "on_tool_end":
                    yield json.dumps({
                                            "event": "end_tool",
                                            "name": event["name"],
                                            "output": event["data"].get("output")
                                        })


        def generate_response_sync(input):
            async_gen = generate_response(input)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                while True:
                    yield loop.run_until_complete(async_gen.__anext__())
            except StopAsyncIteration:
                pass
            finally:
                loop.close()
                
                # elif event["event"] == "on_chat_model_error":
                #     # 保存結果        
                #     bot_message_content = {"role": "assistant","content": response_content}
                #     save_message(user_id, dialogue_id, bot_message_content)
        return StreamWithHeaders(generate_response_sync(input=message), headers=headers, mimetype='text/event-stream')

        
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

