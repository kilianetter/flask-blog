from flask import Flask
# Extensions
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_mail import Mail

# custom
from blog.config import Config


### Register extensions
### Database
db = SQLAlchemy()
### encryption
# how does it work? are there alternatives?
bcrypt = Bcrypt()
### Login Manager
# flask-login
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = "User needs to be logged in to view this page"
login_manager.login_message_category = "warning"
### Mail ###
mail = Mail()


def create_app(config_class = Config):
    ### App 
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Blueprint registration
    from blog.main.routes import main
    from blog.users.routes import users
    from blog.posts.routes import posts
    from blog.errors.handler import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
