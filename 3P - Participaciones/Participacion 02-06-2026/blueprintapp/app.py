from flask import Flask
from blueprintapp.extensions import db,bcrypt,login_manager,migrate
from .miembros.models import Miembro

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = "clave-secreta-123"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bd_equipo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)

    @login_manager.user_loader
    def load_user(user_id):
        return Miembro.query.get(int(user_id))

    from blueprintapp.miembros.routes import bp_miembro
    from blueprintapp.core.routes import bp_core
    from blueprintapp.tareas.routes import bp_tarea
    from blueprintapp.auth.routes import bp_auth

    app.register_blueprint(bp_miembro,url_prefix="/miembro")
    app.register_blueprint(bp_core,url_prefix="/core")
    app.register_blueprint(bp_tarea,url_prefix="/tareas")
    app.register_blueprint(bp_auth,url_prefix="/")
    
    return app

