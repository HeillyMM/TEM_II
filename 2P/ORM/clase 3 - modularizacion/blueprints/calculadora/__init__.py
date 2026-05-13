from flask import Blueprint, render_template, redirect, url_for

calculadora_bp = Blueprint("calculadora", __name__, template_folder="templates")


@calculadora_bp.route("/")
def index():
    return render_template("index.html")


@calculadora_bp.route("/suma/<int:num1>/<int:num2>")
def suma(num1, num2):
    return "Suma "+str(num1+num2)

@calculadora_bp.route("/resta/<int:num1>/<int:num2>")
def resta(num1, num2):
    return "Resta " + str(num1-num2)


    