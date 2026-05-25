from flask import render_template,Blueprint
from blueprintapp.categorias.models import Categoria
from blueprintapp.productos.models import Producto
from blueprintapp.app import db

bp_core = Blueprint('bp_core',__name__,template_folder='templates')

@bp_core.route("/")
def index():
    total_productos = Producto.query.count()

    total_categorias = Categoria.query.count()

    total_stock = db.session.query(db.func.sum(Producto.stock)).scalar()

    return render_template('core/index.html',total_productos=total_productos,
        total_categorias=total_categorias,
        total_stock=total_stock)