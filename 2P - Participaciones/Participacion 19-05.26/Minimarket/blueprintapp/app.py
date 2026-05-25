from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tienda.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from blueprintapp.categorias.routes import bp_categoria
    from blueprintapp.productos.routes import bp_producto
    from blueprintapp.core.routes import bp_core

    app.register_blueprint(bp_categoria,url_prefix='/categorias')
    app.register_blueprint(bp_producto,url_prefix='/productos')
    app.register_blueprint(bp_core,url_prefix='/')

    db.init_app(app)
    migrate.init_app(app,db)

    return app