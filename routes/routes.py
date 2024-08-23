from flask import render_template
from controllers import auth, chat, models, dialogue, user, files
def register_routes(app):
    # 註冊藍圖，並設定統一的請求路徑前綴
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(chat, url_prefix='/chat')
    app.register_blueprint(models, url_prefix='/models')
    app.register_blueprint(user, url_prefix='/users')
    app.register_blueprint(dialogue, url_prefix='/dialogues')
    app.register_blueprint(files, url_prefix='/files')

    # 其他全局的路由或错误处理程序也可以放在这里
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404