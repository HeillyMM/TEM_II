from flask import render_template
from flask_login import login_required # libreria que protege rutas. todas rutas que tienen esto protege las rutas para que entren solo usuarios que esten autenticados
from app.models import User
from app.main import main_bp


@main_bp.route("/")
def index():
    return render_template('main/index.html')

@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html")