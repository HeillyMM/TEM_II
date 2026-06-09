from flask import render_template, redirect,request,url_for,Blueprint
from flask_login import login_required, login_user,logout_user,current_user
from blueprintapp.miembros.models import Miembro
from blueprintapp.app import bcrypt

bp_auth = Blueprint("bp_auth",__name__,template_folder="templates")

@bp_auth.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("auth/login.html")
    elif request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        usuario = Miembro.query.filter_by(email=email).first()
        if usuario and bcrypt.check_password_hash(usuario.password,password):
            login_user(usuario)
            
            if current_user.tipo == "miembro":
                return redirect(url_for('bp_miembro.dashboard'))
            elif current_user.tipo == "admin":
                return redirect(url_for('bp_core.index'))
        return redirect(url_for('bp_auth.login'))
    
@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('bp_auth.login'))