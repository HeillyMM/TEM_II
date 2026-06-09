from flask import request,render_template,redirect,url_for,Blueprint,flash,abort
from flask_login import login_required,current_user
from blueprintapp.app import db,bcrypt
from blueprintapp.miembros.models import Miembro
from blueprintapp.tareas.models import Tarea

bp_miembro = Blueprint('bp_miembro',__name__,template_folder='templates')

@bp_miembro.route("/")
@login_required
def index():
    if current_user.tipo != "admin":
        abort(403)
    miembros = Miembro.query.all()
    return render_template('miembro/index.html',miembros=miembros)

@bp_miembro.route("/dashboard")
@login_required
def dashboard():
    if current_user.tipo != "miembro":
        abort(403)
    total_tareas = Tarea.query.filter_by(id_miembro=current_user.id).count()
    tareas_completadas = Tarea.query.filter_by(completado=True,id_miembro=current_user.id).count()
    return render_template("miembro/dashboard.html",total_tareas=total_tareas,tareas_completadas=tareas_completadas)

@bp_miembro.route("/create",methods=['GET','POST'])
@login_required
def create():
    if current_user.tipo != "admin":
        abort(403)
    if request.method == 'GET':
        return render_template('miembro/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        tipo = request.form.get('tipo')

        if Miembro.query.filter_by(email=email).first():
            flash("este email ya fue registrado con otro miembro","danger")
            return render_template('miembro/create.html')
        
        password_hashed = bcrypt.generate_password_hash(nombre.split()[0].lower()+str(123)).decode("utf-8")
        miembro = Miembro(nombre=nombre,email=email,password=password_hashed,tipo=tipo)
        db.session.add(miembro)
        db.session.commit()

        return redirect(url_for('bp_miembro.index'))
    
@bp_miembro.route("/update/<int:id>",methods=['GET','POST'])
@login_required
def update(id):
    miembro = Miembro.query.get(id)
    if request.method == 'GET':
        return render_template('miembro/update.html',miembro=miembro)
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')

        if Miembro.query.filter_by(email=email).first():
            flash("El email ya está siendo usando en otra cuenta","danger")
            return redirect(url_for('bp_miembro.update',id))
        
        password = request.form.get('password')
        if current_user.tipo == "admin":
            tipo = request.form.get('tipo')
            tipo = tipo

        miembro.nombre = nombre
        miembro.email = email
        password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        db.session.commit()

        return redirect(url_for('bp_miembro.index'))
    
@bp_miembro.route("/miembro/delete/<int:id>")
@login_required
def delete(id):
    if current_user.tipo != "admin":
        abort(403)

    miembro = Miembro.query.get(id)
    if miembro.tipo == "admin" and Miembro.query.filter_by(tipo="admin").count() == 1:
        flash("Solo hay 1 administrador, no se puede eliminar","danger")
        return redirect(url_for('bp_miembro.index'))
    db.session.delete(miembro)
    db.session.commit()

    return redirect(url_for('bp_miembro.index'))