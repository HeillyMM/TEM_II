from flask import render_template,redirect,url_for,request,Blueprint
from blueprintapp.productos.models import Producto
from blueprintapp.categorias.models import Categoria
from blueprintapp.app import db

bp_producto = Blueprint('bp_producto',__name__,template_folder='templates')

@bp_producto.route("/")
def index():
    productos = Producto.query.all()
    return render_template('productos/index.html',productos=productos)

@bp_producto.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        disponible = bool(request.form.get('disponible'))
        id_categoria = request.form.get('id_categoria')

        producto = Producto(nombre=nombre,precio=precio,stock=stock,disponible=disponible,id_categoria=id_categoria)
        db.session.add(producto)
        db.session.commit()

        return redirect(url_for('bp_producto.index'))
    
    categorias = Categoria.query.all()
    return render_template('productos/create.html',categorias=categorias)

@bp_producto.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    producto = Producto.query.get(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        disponible = True if 'disponible' in request.form.keys() else False
        id_categoria = request.form.get('id_categoria')

        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock
        producto.disponible = disponible
        producto.id_categoria = id_categoria
        db.session.commit()

        return redirect(url_for('bp_producto.index'))
    
    categorias = Categoria.query.all()
    return render_template('productos/update.html',categorias=categorias,producto=producto)

@bp_producto.route("/delete/<int:id>")
def delete(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for('bp_producto.index'))