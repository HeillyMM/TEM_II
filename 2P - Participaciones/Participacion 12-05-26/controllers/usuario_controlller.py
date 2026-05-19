from flask import Blueprint, redirect, url_for, request, session, abort
from models.usuario_model import Usuario
from views import usuario_view

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuario_bp.route("/", methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('usuarios.home_view'))

    if request.method == 'GET':
        return usuario_view.login()
        
    username = request.form['username']
    password = request.form['password'] 
    
    usuario_autenticado = Usuario.login(username, password)
    
    if usuario_autenticado:
        session['usuario_id'] = usuario_autenticado.id_usuario
        session['username'] = usuario_autenticado.username
        session['rol'] = usuario_autenticado.rol
        return redirect(url_for('usuarios.home_view'))
    
    return usuario_view.login()

@usuario_bp.route("/home")
def home_view():
    if 'usuario_id' not in session:
        return redirect(url_for('usuarios.login'))
    return usuario_view.home()

@usuario_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('usuarios.login'))

@usuario_bp.route("/menu", methods=['GET'])
def mostrar_usuarios():
    if 'usuario_id' not in session:
        return redirect(url_for('usuarios.login'))
    if session.get('rol') != 'admin':
        return redirect(url_for('usuarios.home_view'))
    lista_usuarios = Usuario.usuarios()
    return usuario_view.mostrar_usuarios(lista_usuarios)


@usuario_bp.route("/actualizar/<int:id>", methods=['GET', 'POST'])
def actualizar_usuario(id):

    if 'usuario_id' not in session:
        return redirect(url_for('usuarios.login'))
    if session.get('rol') != 'admin':
        return redirect(url_for('usuarios.home_view'))

    usuario = Usuario.usuario(id)
    if not usuario:
        abort(404)

    if request.method == 'POST':
        username = request.form.get('username')
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        if not password:
            password = None

        usuario.actualizar(username=username, correo=correo, password=password)

        if usuario.id_usuario == session.get('usuario_id'):
            session['username'] = usuario.username

        return redirect(url_for('usuarios.mostrar_usuarios'))
    return usuario_view.actualizar_usuario(usuario)

@usuario_bp.route("/eliminar/<int:id>")
def eliminar(id):
    usuario = Usuario.usuario(id)
    usuario.eliminar()
    return redirect(url_for('usuarios.mostrar_usuarios'))