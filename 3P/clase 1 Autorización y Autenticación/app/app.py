# Creacion de app usadno aplication factory
from flask import Flask
from flask_migrate import Migrate
from app.extensions import db,bcrypt,login_manager
from app.models import User

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # importacion de blueprints
    from app.main import main_bp
    from app.auth import auth_bp
    # registro de blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    with app.app_context():
        db.create_all()
        
    return app