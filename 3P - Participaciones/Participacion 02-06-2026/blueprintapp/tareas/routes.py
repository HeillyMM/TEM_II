from flask import request,render_template,redirect,url_for,Blueprint,abort
from flask_login import login_required,current_user
from blueprintapp.app import db
from blueprintapp.tareas.models import Tarea
from blueprintapp.miembros.models import Miembro

bp_tarea = Blueprint('bp_tarea',__name__,template_folder='templates')

@bp_tarea.route("/")
@login_required
def index():
    if current_user.tipo == "admin":
        tareas = Tarea.query.all()
    else:
        tareas = Tarea.query.filter_by(id_miembro=current_user.id).all()
    return render_template('tareas/index.html',tareas=tareas)

@bp_tarea.route("/create",methods=['GET','POST'])
@login_required
def create():
    if current_user.tipo != "admin":
        abort(403)
    if request.method == 'GET':
        miembros = Miembro.query.filter_by(tipo="miembro")
        return render_template('tareas/create.html',miembros=miembros)
    elif request.method == 'POST':
        descripcion = request.form.get('descripcion')
        id_miembro = request.form.get('id_miembro')
        completado = True if 'completado' in request.form.keys() else False

        tarea = Tarea(descripcion=descripcion,completado=completado,id_miembro=id_miembro)
        db.session.add(tarea)
        db.session.commit()

        return redirect(url_for('bp_tarea.index'))
    
@bp_tarea.route("/update/<int:id>",methods=['GET','POST'])
@login_required
def update(id):
    if current_user.tipo != "admin":
        abort(403)
    tarea = Tarea.query.get(id)
    if request.method == 'GET':
        miembros = Miembro.query.all()
        return render_template('tareas/update.html',tarea=tarea,miembros=miembros)
    elif request.method == 'POST':
        descripcion = request.form.get('descripcion')
        id_miembro = request.form.get('id_miembro')
        completado = True if 'completado' in request.form.keys() else False

        tarea.descripcion = descripcion
        tarea.completado = completado
        tarea.id_miembro = id_miembro

        db.session.commit()

        return redirect(url_for('bp_tarea.index'))

@bp_tarea.route("/delete/<int:id>")
@login_required
def delete(id):
    if current_user.tipo != "admin":
        abort(403)
    tarea = Tarea.query.get(id)
    db.session.delete(tarea)
    db.session.commit()

    return redirect(url_for('bp_tarea.index'))

@bp_tarea.route("/completado/<int:id_tarea>")
@login_required
def completado(id_tarea):
    tarea = Tarea.query.get(id_tarea)
    if tarea.completado == True:
        tarea.completado = False
    else: 
        tarea.completado = True
    db.session.commit()
    return redirect(url_for('bp_tarea.index'))