from flask import Blueprint, render_template, redirect

hola_mundo_bp = Blueprint("Hola mundo", __name__,template_folder="templates")

@hola_mundo_bp.route("/")
def index():
    return "Hola mundo desde Blueprint"


@hola_mundo_bp.route("/hola/<nombre>")
def hola_nombre(nombre):
    return "Hola "+ nombre + " Bienvenido"


@hola_mundo_bp.route("/hola_html")
def hola_html():
    return render_template("hola.html")
