from flask import Blueprint, render_template, request, Response
from ..models.llm_config.model_list import get_model
import json
from ..models.agent_chat import agent_executor

agentChat_bp = Blueprint('agent_chat', __name__)

@agentChat_bp.route('/agent_chat', methods=['GET', 'POST'])
def agent_chat():
    if request.method == 'POST':
        # 提取所有值
        history = json.loads(request.form.get('history'))  # 假设 history 是以 JSON 字符串形式传递的
        message = request.form.get('message')
        model_type = request.form.get('model_type')
        model_name = request.form.get('model_name')
        api_key = request.form.get('api_key')

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

        # # 模拟机器人的响应
        # llm = get_model(model_type=model_type,model_name=model_name,api_key=api_key)

        # def generate_response(message):
        #     for chunk in llm.stream(message):
        #         yield chunk.content   

        def generate_response(message):
            for chunk in agent_executor.stream({"input": message}):
                if "actions" in chunk:
                    for action in chunk["actions"]:
                        info = f"Calling Tool: `{action.tool}` with input `{action.tool_input}`\\n"
                        # print(info)
                        yield info
                # elif "steps" in chunk:
                #     print(chunk["steps"])
                #     # for step in chunk["steps"]:
                #     #     yield step.observation
                #     # yield chunk["steps"]
                elif "output" in chunk:
                    yield chunk["output"]
                # yield f"data: {chunk.content}\n\n".encode('utf-8')  # 确保生成的内容是字节格式

        return Response(generate_response(message=message), mimetype='text/event-stream')
        
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