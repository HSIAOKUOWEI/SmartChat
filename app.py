import os
from dotenv import load_dotenv
# 加载 .env 文件
load_dotenv()

from flask import Flask, request, redirect, url_for, jsonify
import time

from models.utils.jwt_utils import verify_token, refresh_token_expiry
from routes.routes import register_routes


app = Flask(__name__, static_folder='static', static_url_path='/static')


def cache_bust(url):
    """Filter to append a timestamp to static file URLs to prevent caching."""
    return f"{url}?v={int(time.time())}"


def create_app(app=app):

    # 添加缓存清除过滤器
    app.jinja_env.filters['cache_bust'] = cache_bust

    # 请求正式處理前的验证和更新token過期時間
    @app.before_request
    async def check_and_refresh_token():
        print(f"Request path: {request.path}, Endpoint: {request.endpoint}") 
        # 排除不需要驗證的endpoint：藍圖名稱.路由函數名稱
        if request.endpoint in ['auth.login', 'users.register','users.password', 'static']:
            return
        
        # 從請求中取得 'token' 
        token = request.cookies.get('token')
        # 驗證 token
        verify = verify_token(token)
        # 驗證失敗，重定向到登入頁面
        if not verify["success"]:
            # 已登錄狀態，但token過期
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # print("hello")
                return jsonify({"redirect": url_for('auth.login')}), 401
            else:
                # 未登錄狀態，直接跳轉到登錄頁面
                return redirect(url_for('auth.login'))

    # 請求處理完後，檢查token是否小於10分鐘，如果小於10分鐘則刷新token，並更新請求的token
    @app.after_request
    def refresh_token(response):
        token = request.cookies.get('token')
        if token:
            new_token = refresh_token_expiry(token=token,
                                             token_renewal_threshold_minutes=10, # 10分鐘內過期既刷新token
                                             extension_hours=1 # 設置新的token過期時間為1小時
                                             )
            # 將新token添加到請求上               
            if new_token:
                # print(new_token)
                response.set_cookie('token', new_token, httponly=True, secure=True)
        return response
            
    # 注冊所有路由
    register_routes(app)
    return app

if __name__ == '__main__':
    import os
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT'))
    debug = os.getenv('FLASK_DEBUG').lower() in ['true', '1', 't', 'yes', 'y']
    
    app = create_app()
    app.run(host=host,port=port, debug=debug)

