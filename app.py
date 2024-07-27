from flask import Flask, request, redirect, url_for, jsonify
from controllers.auth import auth_bp
from controllers.agent_chat import agentChat_bp
from controllers.get_model_list import modelList_bp
from controllers.users import user_bp
import time
from models.until.jwt_utils import verify_token, refresh_token_expiry

def cache_bust(url):
    """Filter to append a timestamp to static file URLs to prevent caching."""
    return f"{url}?v={int(time.time())}"



def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')


    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(agentChat_bp)
    app.register_blueprint(modelList_bp)
    app.register_blueprint(user_bp)

    
    # 添加缓存清除过滤器
    app.jinja_env.filters['cache_bust'] = cache_bust

    # 全局请求前的验证和更新token过期时间
    @app.before_request
    def check_and_refresh_token():
        # 排除不需要验证和更新的endpoint
        if request.endpoint in ['auth.login', 'auth.generate_token', 'user.register','user.forgot_password', 'static']:
            return

        # 从请求中获取 'token' 的 cookie 值
        token = request.cookies.get('token')
        # 验证 token
        verify = verify_token(token)
        # 验证失败，重定向到登录页面
        if not verify["success"]:
            print("Invalid or expired token, redirecting to login.")
            return redirect(url_for('auth.login'))

        # 更新 token 过期时间
        if token:
            new_token = refresh_token_expiry(token)
            if new_token:
                # 更新cookie中的token
                response = jsonify({"message": "Token refreshed"})
                response.set_cookie('token', new_token)
                return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
