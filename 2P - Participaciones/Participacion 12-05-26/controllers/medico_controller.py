from flask import request,redirect,url_for,Blueprint
from models.medico_model import Medico
from views import medico_view

medico_bp = Blueprint('medico',__name__,url_prefix='/medicos')

@medico_bp.route("/")
def menu():
    medicos = Medico.medicos()
    return medico_view.menu(medicos)

@medico_bp.route("/editar/<int:id>",methods=['GET','POST'])
def editar(id):
    medico = Medico.medico(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        medico.actualizar(nombre,especialidad,telefono,correo)

        return redirect(url_for('medico.menu'))
    return medico_view.editar_medico(medico)


@medico_bp.route("/registrar",methods=['GET','POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        correo = request.form['correo']

        medico = Medico(nombre,especialidad,telefono,correo)
        medico.guardar()

        return redirect(url_for('medico.menu'))
    
    return medico_view.registrar_medico()

@medico_bp.route("/eliminar/<int:id>")
def eliminar(id):
    medico = Medico.medico(id)
    medico.eliminar()

    return redirect(url_for('medico.menu'))