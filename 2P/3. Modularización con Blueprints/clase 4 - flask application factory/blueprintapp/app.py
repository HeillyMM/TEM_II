from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_equipo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    # 1. Importación del blueprint (Para cada modulo)
    from blueprintapp.miembros.routes import bp_miembro
    from blueprintapp.core.routes import bp_core
    from blueprintapp.tareas.routes import bp_tarea
    
    # 2. Registrar el blueprint (Para cada modulo)
    app.register_blueprint(bp_miembro,url_prefix="/miembros")
    app.register_blueprint(bp_core,url_prefix="/")
    app.register_blueprint(bp_tarea,url_prefix="/tareas")
    
    return app