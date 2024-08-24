import os
import time
from dotenv import load_dotenv
# 加載 .env 文件，確保在導入其他模塊之前加載環境變量
load_dotenv(dotenv_path='.env')

from flask import Flask, request, redirect, url_for, jsonify
from models.utils.jwt_utils import verify_token, refresh_token_expiry
from routes.routes import register_routes

# 創建 Flask 應用實例
app = Flask(__name__, static_folder='static', static_url_path='/static')

# 添加緩存清除過濾器
app.jinja_env.filters['cache_bust'] = lambda url: f"{url}?v={int(time.time())}"

# 請求前驗證和更新 token 過期時間
@app.before_request
async def check_and_refresh_token():
    print(f"Request path: {request.path}, Endpoint: {request.endpoint}") 
    if request.endpoint in ['auth.login', 'users.register', 'users.password', 'static']:
        return

    token = request.cookies.get('token')
    verify = verify_token(token)
    if not verify["success"]:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"redirect": url_for('auth.login')}), 401
        return redirect(url_for('auth.login'))

# 請求後刷新 token
@app.after_request
def refresh_token(response):
    token = request.cookies.get('token')
    if token:
        new_token = refresh_token_expiry(token, token_renewal_threshold_minutes=10, extension_hours=1)
        if new_token:
            response.set_cookie('token', new_token, httponly=True, secure=True)
    return response

# 註冊所有路由
register_routes(app)

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST', '127.0.0.1'), 
            port=int(os.getenv('FLASK_PORT', 5000)), 
            debug=os.getenv('FLASK_DEBUG', 'false').lower() in ['true', '1', 't', 'yes', 'y'])
