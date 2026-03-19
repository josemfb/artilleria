from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)

    # Register Blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
