from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.login_message_category = "aviso"


def create_app(config_class=None):
    from config import Config

    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    from app.controllers.main import bp as main_bp
    from app.controllers.auth import bp as auth_bp
    from app.controllers.livros import bp as livros_bp
    from app.controllers.emprestimos import bp as emprestimos_bp
    from app.controllers.feedback import bp as feedback_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(livros_bp)
    app.register_blueprint(emprestimos_bp)
    app.register_blueprint(feedback_bp)

    @app.errorhandler(403)
    def proibido(e):
        return render_template("erro.html", codigo=403,
                               mensagem="Você não tem permissão para acessar esta página."), 403

    @app.errorhandler(404)
    def nao_encontrado(e):
        return render_template("erro.html", codigo=404,
                               mensagem="Página não encontrada."), 404

    @app.errorhandler(413)
    def muito_grande(e):
        return render_template("erro.html", codigo=413,
                               mensagem="Arquivo muito grande. O limite é 2 MB."), 413

    @app.errorhandler(500)
    def erro_interno(e):
        db.session.rollback()
        return render_template("erro.html", codigo=500,
                               mensagem="Erro interno. Tente novamente em instantes."), 500

    from app.seed import register_commands
    register_commands(app)

    with app.app_context():
        db.create_all()

    return app
