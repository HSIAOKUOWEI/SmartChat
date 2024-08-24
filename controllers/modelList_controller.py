from flask import Blueprint, jsonify
from models.model_list import MODEL_LIST_DETAILS

models = Blueprint('models', __name__)
@models.route('/models', methods=['GET'])
def get_model_list():
    # 將模型列表轉換為帶有順序資訊的數組
    ordered_model_list = [
        {"category": category, "models": [{"name": name, "value": value} for name, value in models.items()]}
        for category, models in MODEL_LIST_DETAILS.items()
    ]

    return jsonify(ordered_model_list)