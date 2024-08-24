from flask import Blueprint, request, jsonify
from models.dialogue import (
    get_user_dialogues, #獲取對話框
    get_dialogue_messages, #獲取對話框內消息
    delete_dialogue_and_messages, # 刪除對話框和對話框的消息
    update_dialogue_title, # 更新對話框名稱
    save_message, #儲存消息
    get_user_id, #獲取user_id
)

# 建立藍圖
dialogue = Blueprint('dialogue', __name__)

# 獲取所有對話框
@dialogue.route('/', methods=['GET'])
def get_dialogues():
    try:
        token = request.cookies.get('token')
        user_id = get_user_id(token)
        dialogues = get_user_dialogues(user_id)
        # print(dialogues)
        return jsonify(dialogues), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# 獲取對話框内容
@dialogue.route('/<dialogue_id>/messages', methods=['GET'])
def get_messages(dialogue_id):
    try:
        token = request.cookies.get('token')
        user_id = get_user_id(token)
        messages = get_dialogue_messages(user_id, dialogue_id)
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# 刪除對話框和對話框內消息
@dialogue.route('/<dialogue_id>', methods=['DELETE'])
def delete_dialogue(dialogue_id):
    try:
        token = request.cookies.get('token')
        user_id = get_user_id(token)
        delete_dialogue_and_messages(user_id, dialogue_id)
        return jsonify({"message": "Dialogue and messages deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# 更新對話框標題
@dialogue.route('/<dialogue_id>/title', methods=['PUT'])
def update_title(dialogue_id):
    try:
        token = request.cookies.get('token')
        user_id = get_user_id(token)
        data = request.get_json()
        new_title = data.get('new_title')
        update_dialogue_title(user_id, dialogue_id, new_title)
        return jsonify({"message": "Dialogue title updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400