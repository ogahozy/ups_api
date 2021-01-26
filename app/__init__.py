import os
from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from config import Config

bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
   
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

   
