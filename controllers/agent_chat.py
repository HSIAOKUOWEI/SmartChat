from flask import Blueprint, render_template, request, jsonify, redirect, url_for, Response
from models.llm_config.model_list import get_model



agentChat_bp = Blueprint('agent_chat', __name__)

@agentChat_bp.route('/agent_chat', methods=['GET', 'POST'])
def agent_chat():
    if request.method == 'POST':
        # 打印接收到的FormData数据
        print("Received FormData:")
        for key, value in request.form.items():
            print(f"{key}: {value}")

        # 提取文字消息
        message = request.form.get('message')
        
        # 提取文件和图片
        files = request.files.getlist('files')
        images = request.form.getlist('images')

        # 打印接收到的数据
        print("Received message:", message)
        print("Received files:", [file.filename for file in files])
        print("Received images:", images)

        # 模拟机器人的响应
        llm = get_model(model_type="Google",model_name="gemini-1.5-pro",api_key=None)

        def generate_response(message):
            for chunk in llm.stream(message):
                yield chunk.content

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

