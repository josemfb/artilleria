from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from app.utils import validate_and_format_run
from config import Config


class Base(DeclarativeBase):
    """
    Clase base declarativa, para evitar problemas con MyPy.
    """

    pass


# Inicializar extensiones
db = SQLAlchemy(model_class=Base)
login = LoginManager()
login.login_view = "auth.login"
login.login_message = ""


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registrar template filters
    @app.template_filter("format_run")
    def format_run_filter(run_str):
        try:
            return validate_and_format_run(run_str, points=True)
        except ValueError:
            return run_str

    # Inicializar extensiones de Flask
    db.init_app(app)
    login.init_app(app)

    from app.models import Usuario

    @login.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Registrar Blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.settings import settings_bp
    from .routes.volunteers import volunteers_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(volunteers_bp)

    # Registrar comandos CLI
    from .cli import create_admin, init_db

    app.cli.add_command(create_admin)
    app.cli.add_command(init_db)

    return app
