from flask import Blueprint, render_template, request, jsonify, Response
import os
from werkzeug.utils import secure_filename
import time
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.model_details import groq_api_key,google_api_key

chatbot_bp = Blueprint('multiChatbot', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pdf', 'pptm', 'pptx'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # 直接覆盖已有文件
    file.save(file_path)
    return file_path

@chatbot_bp.route('/chatbot', methods=['GET'])
def chat():
    return render_template('chatchat.html')

def stream_response(message, prefix):
    for i in range(5):
        yield f"{prefix}: Part {i + 1} of response for message: {message}\n"
        time.sleep(1)  # Simulate delay

@chatbot_bp.route('/chatbot/Gemini_1.5_Pro', methods=['POST'])
def gemini_1_5_pro():
    user_message = request.json.get('message', '')
    llm = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=google_api_key)
    prompt = ChatPromptTemplate.from_messages([("human", "{topic}")])
    chain = prompt | llm
    def generate(topic):
        for chunk in chain.stream({"topic": topic}):
            yield chunk

    return Response(generate(topic=user_message), mimetype='text/event-stream')

@chatbot_bp.route('/chatbot/LLaMA3_70b', methods=['POST'])
def llama3_70b():
    user_message = request.form.get('message', '')
    files = request.files.getlist('files[]')
    images = request.files.getlist('images[]')

    saved_files = []
    saved_images = []

    for file in files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            saved_files.append(file_path)

    for image in images:
        if allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            saved_images.append(image_path)
    
    # 將文件和圖片路徑添加到用戶消息中
    file_info = "\n".join([f"Uploaded file: {file}" for file in saved_files])
    image_info = "\n".join([f"Uploaded image: {image}" for image in saved_images])
    full_message = f"{user_message}\n{file_info}\n{image_info}".strip()

    chat = ChatGroq(groq_api_key=groq_api_key, model="llama3-70b-8192",temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([("human", "{topic}")])
    chain = prompt | chat
    def generate(topic):
        for chunk in chain.stream({"topic": topic}):
            yield chunk.content

    return Response(generate(topic=user_message), mimetype='text/event-stream')

@chatbot_bp.route('/chatbot/LLaMA3_8b', methods=['POST'])
def llama3_8b():
    user_message = request.json.get('message', '')
    chat = ChatGroq(groq_api_key=groq_api_key, model="llama3-8b-8192",temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([("human", "{topic}")])
    chain = prompt | chat
    def generate(topic):
        for chunk in chain.stream({"topic": topic}):
            yield chunk.content

    return Response(generate(topic=user_message), mimetype='text/event-stream')

@chatbot_bp.route('/chatbot/Mixtral_8_7b', methods=['POST'])
def mixtral_8_7b():
    user_message = request.json.get('message', '')
    chat = ChatGroq(groq_api_key=groq_api_key, model="mixtral-8x7b-32768",temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([("human", "{topic}")])
    chain = prompt | chat
    def generate(topic):
        for chunk in chain.stream({"topic": topic}):
            yield chunk.content

    return Response(generate(topic=user_message), mimetype='text/event-stream')

