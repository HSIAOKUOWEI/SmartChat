from flask import render_template, redirect, url_for
from controllers import auth, chat, models, dialogue, users, files
def register_routes(app):
    # 註冊藍圖，並設定統一的請求路徑前綴
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(chat, url_prefix='/chat')
    app.register_blueprint(models, url_prefix='/models')
    app.register_blueprint(dialogue, url_prefix='/dialogues')
    app.register_blueprint(files, url_prefix='/files')

    
    # 根路由，重導向到登錄頁面
    @app.route('/')
    async def root():
        return redirect(url_for('auth.login')) # 藍圖.路由函數名稱
    
    # 其他全域的路由或錯誤處理程序也可以放在這裡
    @app.errorhandler(404)
    async def page_not_found(e):
        return render_template('404.html'), 404