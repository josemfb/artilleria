from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

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
