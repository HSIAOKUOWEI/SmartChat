from flask import Blueprint, render_template, request, Response
from models.llm_config.model_list import get_model
import json
from models.agent_chat import agent_executor
from models.crud_history import save_message,get_user_id



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


        # # 模拟机器人的响应
        # llm = get_model(model_type=model_type,model_name=model_name,api_key=api_key)

        # def generate_response(message):
        #     for chunk in llm.stream(message):
        #         yield chunk.content   

        def generate_response(message):
            for chunk in agent_executor.stream({"input": message}):
                response_content = ""
                if "actions" in chunk:
                    for action in chunk["actions"]:
                        info = f"Calling Tool: `{action.tool}` with input `{action.tool_input}`\\n"
                        # 逐字输出
                        for char in info:
                            yield char
                        yield "action_result_finish"  
                elif "steps" in chunk:
                    for step in chunk["steps"]:
                        # 逐字输出 observation 内容
                        observation = step.observation
                        for char in observation:
                            yield char
                        yield 'tool_result_finish' 
                elif "output" in chunk:
                    output = chunk["output"]
                    response_content += output
                    for char in output:
                        yield char
                    yield '\n'  # 添加换行符以区分不同步骤的结果  
            # 保存結果        
            bot_message_content = {"role": "assistant","content": response_content}
            save_message(user_id, dialogue_id, bot_message_content)
        # return Response(generate_response(message=message), mimetype='text/event-stream')
        return StreamWithHeaders(generate_response(message=message), headers=headers, mimetype='text/event-stream')

        
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

# def generate_response(message):
#     for chunk in llm.stream({"input": message}):
#         if "actions" in chunk:
#             for action in chunk["actions"]:
#                 info = f"Calling Tool: `{action.tool}` with input `{action.tool_input}`"
#                 print(info)
#                 yield f"data: {info}\n\n".encode('utf-8')
#         elif "steps" in chunk:
#             for step in chunk["steps"]:
#                 info = f"Tool Result: `{step.observation}`"
#                 print(info)
#                 yield f"data: {info}\n\n".encode('utf-8')
#         elif "output" in chunk:
#             info = f'Final Output: {chunk["output"]}'
#             print(info)
#             yield f"data: {info}\n\n".encode('utf-8')
#         yield f"data: {chunk.content}\n\n".encode('utf-8')  # 确保生成的内容是字节格式