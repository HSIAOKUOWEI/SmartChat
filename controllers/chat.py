from flask import Blueprint, render_template, request, Response

from models.llm_config.model_list import get_model
from models.agent_chat import agentChat_response_sync
from models.crud_history import save_message,get_user_id
import json

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

        # 保存用戶訊息，如對話框為空，則返回新創的對話框id
        dialogue_id = save_message(user_id, dialogue_id, user_message_content)
        headers = {"dialogue_id": dialogue_id} # 返回給前端
                
        return StreamWithHeaders(agentChat_response_sync(userid = user_id, 
                                                         dialogueid = dialogue_id , 
                                                         history = history , # 歷史消息
                                                         message = message,  # 當前消息
                                                         files = files, 
                                                         images = images), headers=headers, mimetype='text/event-stream')
        
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

