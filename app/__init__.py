from flask import Flask
from .config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

#Instantiate flask_migrate and flask_sqlalchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Instantiate login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#csrf = CSRFProtect(app)
CORS(app)

from app import views
from app import models