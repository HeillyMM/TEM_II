# Importacion de libs
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
#pantilla q va a usar para autentificar
login_manager.login_view = "auth.login"