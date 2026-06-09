from flask import render_template,request,redirect,url_for,flash # --> envia mensajes a siguien te instancia/procesos
from flask_login import login_user,logout_user,login_required
"""--> mantiene los valores del estaso del login"""

from app.extensions import db,bcrypt
from app.auth import auth_bp
from app.models import User

@auth_bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            flash("El nombre del usuario ya existe","danger")
            return redirect(url_for('auth_bp.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(username=username,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash("usuario registrado exitosamente","success")
        return redirect(url_for('auth_bp.login'))
    
    return render_template('auth/register.html')

@auth_bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            flash("usuario logueado","success")

            return redirect(url_for("main_bp.dashboard"))
        
        flash("usuario o contraseña incorrectos","danger")
    
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))