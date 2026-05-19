from flask import render_template

def mostrar_usuarios(usuarios):
    return render_template("/usuarios/menu.html", usuarios=usuarios)

def actualizar_usuario(usuario):
    return render_template("/usuarios/actualizar.html", usuario=usuario)

def login():
    return render_template("usuarios/login.html")

def home():
    return render_template("home.html")