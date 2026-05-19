from flask import request,url_for,redirect,Blueprint
from models.paciente_model import Paciente 
from views import paciente_view

paciente_bp = Blueprint('paciente',__name__,url_prefix='/pacientes')

@paciente_bp.route("/")
def menu():
    pacientes = Paciente.pacientes()
    return paciente_view.menu(pacientes)

@paciente_bp.route("/crear",methods=['GET','POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        paciente = Paciente(nombre,edad,direccion,telefono)
        paciente.guardar()

        return redirect(url_for('paciente.menu'))
    return paciente_view.crear()

@paciente_bp.route("/actualizar/<int:id>",methods=['GET','POST'])
def actualizar(id):
    paciente = Paciente.paciente(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        paciente.actualizar(nombre,edad,direccion,telefono)

        return redirect( url_for('paciente.menu') )
    return paciente_view.actualizar(paciente)

@paciente_bp.route("/eliminar/<int:id>")
def eliminar(id):
    paciente = Paciente.paciente(id)
    paciente.eliminar()
    return redirect( url_for('paciente.menu') )

@paciente_bp.route("/consultas/<int:id>")
def consulta(id):
    paciente = Paciente.paciente(id)
    consultas = paciente.consultas_paciente()
    return paciente_view.consultas(consultas)