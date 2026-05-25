from flask import render_template,redirect,url_for,request,Blueprint
from blueprintapp.categorias.models import Categoria
from blueprintapp.app import db

bp_categoria = Blueprint('bp_categoria',__name__,template_folder='templates')

@bp_categoria.route("/")
def index():
    categorias = Categoria.query.all()
    return render_template('categorias/index.html',categorias=categorias)

@bp_categoria.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        categoria = Categoria(nombre=nombre,descripcion=descripcion)
        db.session.add(categoria)
        db.session.commit()

        return redirect(url_for('bp_categoria.index'))
    return render_template('categorias/create.html')

@bp_categoria.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        db.session.commit()

        return redirect(url_for('bp_categoria.index'))
    return render_template('categorias/update.html',categoria=categoria)

@bp_categoria.route("/delete/<int:id>")
def delete(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()

    return redirect(url_for('bp_categoria.index'))