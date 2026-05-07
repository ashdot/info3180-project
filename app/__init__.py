from flask import Flask
from .config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)

#Instantiate flask_migrate and flask_sqlalchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Instantiate login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

#csrf = CSRFProtect(app)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

from app import views
from app import models