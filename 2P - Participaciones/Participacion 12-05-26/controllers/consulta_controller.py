# crear consulta -> medico
# editar consulta -> médico
# ver consulta -> medico y admin
# Eliminar consulta -> medico
from flask import redirect,url_for,request,Blueprint
from models.consulta_model import Consulta
from models.paciente_model import Paciente
from models.usuario_model import Usuario
from models.medico_model import Medico
from models.cita_model import Cita
from views import consulta_view
from controllers.usuario_controlller import session
from datetime import datetime

consulta_bp = Blueprint('consulta',__name__,url_prefix='/consultas')

@consulta_bp.route("/",methods=['GET','POST'])
def menu():
    if request.method == 'POST':
        fecha_str = request.form["fecha"]
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        consultas = Consulta.consulta_fecha(fecha) 
    else:    
        usuario = Usuario.usuario_medico(session['username'])
        if usuario.rol == 'admin':
            consultas = Consulta.query.all()
        else:
            medico = Medico.medico(id=usuario.id_medico)
            consultas = Consulta.consulta_medico(medico.id_medico)
    return consulta_view.menu(consultas)

@consulta_bp.route("/actualizar/<int:id>",methods=['GET','POST'])
def actualizar(id):
    consulta = Consulta.consulta(id)
    pacientes = Paciente.pacientes()
    if request.method == 'POST':
        usuario = Usuario.usuario_medico(session['username'])
        medico = Medico.medico(id=usuario.id_medico)
                               
        fecha_str = request.form["fecha"]
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        id_paciente = request.form['id_paciente']
        id_medico = medico.id_medico
        
        consulta.actualizar(fecha,diagnostico,tratamiento,id_paciente,id_medico)
        return redirect( url_for('consulta.menu') )
    return consulta_view.actualizar(consulta=consulta,pacientes=pacientes)

@consulta_bp.route("/crear",methods=['GET','POST'])
def crear():
    pacientes = Paciente.pacientes()
    usuario = Usuario.usuario_medico(session['username'])
    medico = Medico.medico(id=usuario.id_medico)
    
    if request.method == 'POST':

        fecha_str = request.form["fecha"]
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        id_paciente = request.form['id_paciente']
        id_medico = medico.id_medico
        
        id_cita_seleccionada = request.form['id_cita']
        cita_asociada = Cita.cita(id_cita_seleccionada)
        cita_asociada.actualizar(estado="completada")

        consulta = Consulta(fecha,diagnostico,tratamiento,id_cita_seleccionada,id_paciente,id_medico)
        consulta.guardar()

        return redirect( url_for('consulta.menu') )
    
    citas_disponibles = Cita.query.filter_by(id_medico=medico.id_medico, estado="pendiente").all()
    return consulta_view.crear(pacientes,citas_disponibles)

@consulta_bp.route("/eliminar/<int:id>")
def eliminar(id):
    consulta = Consulta.consulta(id)
    consulta.eliminar()
    return redirect( url_for('consulta.menu') )
