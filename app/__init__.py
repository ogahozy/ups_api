import os
from flask import Flask, request, current_app
#from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# ,login_required,login_user,logout_user
from config import Config

#bootstrap = Bootstrap()
bcrypt = Bcrypt()
db = SQLAlchemy()  #
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
   
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

from app import model

   
