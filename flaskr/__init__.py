import os
from flask import Flask, render_template
from pathlib import Path
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .Models.models import app_config

# Set env directory
env_folder = Path(Path(__file__).parent).parent
env_file = os.path.join(env_folder, '.env')
load_dotenv(dotenv_path=env_file)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()


def create_app():
    # Create app
    app = Flask(__name__, static_folder="frontend/static", template_folder="frontend")

    # Setup Database, LoginManager, and Bcrypt
    app_config(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Setup CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(resp):
        resp.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
        resp.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS,PATCH')

        return resp

    # Register BluePrints
    from flaskr.Errors.handlers import errors
    from flaskr.Users.routes import users

    app.register_blueprint(errors)
    app.register_blueprint(users)


    @app.route('/')
    def index():
    	return render_template("index.html")

    return app
