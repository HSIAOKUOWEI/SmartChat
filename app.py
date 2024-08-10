from flask import Flask, request, redirect, url_for, jsonify
import time
from models.until.jwt_utils import verify_token, refresh_token_expiry
from routes import register_routes

def cache_bust(url):
    """Filter to append a timestamp to static file URLs to prevent caching."""
    return f"{url}?v={int(time.time())}"


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # 添加缓存清除过滤器
    app.jinja_env.filters['cache_bust'] = cache_bust

    # 全局请求前的验证和更新token過期時間
    @app.before_request
    def check_and_refresh_token():
        # 排除不需要验证和更新的endpoint
        if request.endpoint in ['auth.login', 'user.register','user.updatePassword', 'static']:
            return
        
        # 从请求中获取 'token' 的 cookie 值
        token = request.cookies.get('token')
        # 验证 token
        verify = verify_token(token)
        # 验证失败，重定向到登录页面
        if not verify["success"]:
            # 已登錄狀態，使用中token過期
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"redirect": url_for('auth.login')}), 401
            else:
                # 未登錄狀態，直接跳轉到登錄頁面
                return redirect(url_for('auth.login'))

    # 响应后刷新token过期时间并更新响应
    @app.after_request
    def refresh_token(response):
        token = request.cookies.get('token')
        if token:
            new_token = refresh_token_expiry(token=token,
                                             token_renewal_threshold_minutes=10, # 10分鐘內過期既刷新token
                                             extension_hours=1 # 設置新的token過期時間為1小時
                                             )
            # 更新响应的cookie                
            if new_token:
                response.set_cookie('token', new_token, httponly=True, secure=True)
        return response
            
    # 注冊路由
    register_routes(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0",port=5000,debug=True)
