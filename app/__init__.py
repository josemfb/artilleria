from flask import Flask
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


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones de Flask
    db.init_app(app)

    # Registrar Blueprints
    from .routes.main import main_bp

    app.register_blueprint(main_bp)

    # Registrar comandos CLI
    from .cli import create_admin

    app.cli.add_command(create_admin)

    return app
