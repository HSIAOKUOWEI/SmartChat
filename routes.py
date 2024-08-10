from flask import render_template
from controllers import auth_bp, chat_bp, modelList_bp, dialogue_bp, user_bp, file_bp
def register_routes(app):
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(modelList_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(dialogue_bp)
    app.register_blueprint(file_bp)

    # 其他全局的路由或错误处理程序也可以放在这里
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404