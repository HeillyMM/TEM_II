from flask import redirect, url_for, request, Blueprint
from controllers.usuario_controlller import session
from models.cita_model import Cita
from models.usuario_model import Usuario
from models.paciente_model import Paciente
from models.medico_model import Medico
from views import cita_view

cita_bp = Blueprint('cita', __name__, url_prefix='/citas')

@cita_bp.route("/", methods=['GET', 'POST'])
def menu():
    # Seguridad básica: Si no hay sesión iniciada, puedes redirigir al login
    if not session.get('rol'):
        return redirect(url_for('usuario.login')) # Ajusta a tu ruta real de login
        
    pacientes = Paciente.pacientes()
    
    if request.method == 'POST':
        estado = request.form.get('estado')
        id_paciente = request.form.get('id_paciente')
        
        if session.get('rol') == 'admin':
            # El administrador filtra sobre todas las citas del hospital
            citas = Cita.filtrar_citas(estado=estado, id_paciente=id_paciente)
        else:
            # El médico solo filtra sobre sus propias citas asignadas
            usuario = Usuario.usuario_medico(session.get('username'))
            if usuario is not None:
                citas = Cita.filtrar_citas(estado=estado, id_paciente=id_paciente, id_medico=usuario.id_medico)
            else:
                citas = [] # Resguardo en caso de que el usuario médico no exista en BD
                
    else:
        # Lógica original para la carga inicial con GET
        if session.get('rol') == 'admin':
            citas = Cita.citas()
        else:    
            usuario = Usuario.usuario_medico(session.get('username'))
            if usuario is not None:
                citas = Cita.query.filter_by(id_medico=usuario.id_medico).all()
            else:
                citas = []
                
    return cita_view.menu(citas, pacientes=pacientes)

@cita_bp.route("/actualizar/<int:id>", methods=['GET', 'POST'])
def actualizar(id):
    cita = Cita.cita(id)
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        motivo = request.form.get('motivo')
        estado = request.form.get('estado')
        id_paciente = request.form.get('id_paciente')
        id_medico = request.form.get('id_medico')

        cita.actualizar(
            fecha=fecha, 
            hora=hora, 
            motivo=motivo, 
            estado=estado, 
            id_paciente=id_paciente, 
            id_medico=id_medico
        )

        return redirect(url_for('cita.menu'))
    
    pacientes = Paciente.pacientes()
    medicos = Medico.medicos()
    return cita_view.actualizar(cita, pacientes, medicos)

@cita_bp.route("/crear", methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        motivo = request.form.get('motivo')

        id_paciente = request.form.get('id_paciente')
        id_medico = request.form.get('id_medico')

        cita = Cita(fecha, hora, motivo, id_paciente, id_medico)
        cita.crear()

        return redirect(url_for('cita.menu'))

    pacientes = Paciente.pacientes()
    medicos = Medico.medicos()
    return cita_view.crear(pacientes, medicos)

@cita_bp.route("/eliminar/<int:id>")
def eliminar(id):
    cita = Cita.cita(id)
    if cita and session.get('rol') == 'admin':
        cita.eliminar()
    return redirect(url_for('cita.menu'))