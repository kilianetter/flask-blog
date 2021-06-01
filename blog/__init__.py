from flask import Flask

# Extensions
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_mail import Mail

from dotenv import load_dotenv
import os

### App 
app = Flask(__name__)

### Config
# provide secret key 
# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY']= 'herbert'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

load_dotenv()

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_ADDRESS'] = os.environ.get('MAIL_ADDRESS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

### Register extensions
### Database
db = SQLAlchemy(app)
### encryption
# how does it work? are there alternatives?
bcrypt = Bcrypt(app)
### Login Manager
# flask-login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "User needs to be logged in to view this page"
login_manager.login_message_category = "warning"
### Mail ###
mail = Mail(app)


### Import routes
from blog import routes