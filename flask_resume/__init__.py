from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_uploads import configure_uploads, patch_request_class
from flask_login import LoginManager

import os
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES

#######################
#### Configuration ####
#######################

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
AVATARS = UploadSet('avatars', IMAGES, default_dest=lambda x: 'avatars')

######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app

##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)

    csrf.init_app(app)

    db.init_app(app)
    
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'users.login'
    login_manager.init_app(app=app)
    # Flask-Login configuration
    from flask_resume.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Configurate avatar photos storage location
    configure_uploads(app, AVATARS)
    patch_request_class(app)  # set maximum file size, default is 16MB)
    app.app_context().push()

    if app.config.get('TESTING', False):
        db.create_all()

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from flask_resume.recipes import recipes_blueprint
    from flask_resume.users import users_blueprint

    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(users_blueprint)
