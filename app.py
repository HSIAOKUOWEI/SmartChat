from flask import Flask, redirect, url_for, request
from controllers.login import auth_bp
# from controllers.chatbot import chatbot_bp
from controllers.chat import chatbot_bp
import time

from models.jwt_utils import verify_token

def cache_bust(url):
    """Filter to append a timestamp to static file URLs to prevent caching."""
    return f"{url}?v={int(time.time())}"



def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')


    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(chatbot_bp)
    # app.register_blueprint(chatbot_bpp)
    
    # 添加缓存清除过滤器
    app.jinja_env.filters['cache_bust'] = cache_bust

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
