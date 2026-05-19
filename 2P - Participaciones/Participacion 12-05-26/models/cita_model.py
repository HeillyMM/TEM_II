from database import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = "citas"

    id_citas = db.Column(db.Integer,primary_key=True)
    fecha = db.Column(db.Date,nullable=False)
    hora = db.Column(db.Time,nullable=False)
    motivo = db.Column(db.String(200))
    estado = db.Column(db.String(10),nullable=False,default="pendiente")
    id_paciente = db.Column(db.Integer,db.ForeignKey('pacientes.id_paciente'))
    id_medico = db.Column(db.Integer,db.ForeignKey('medicos.id_medico'))

    paciente = db.relationship('Paciente',back_populates='citas')
    medico = db.relationship('Medico',back_populates='citas')
    consulta = db.relationship('Consulta', back_populates='cita')

    def __init__(self,fecha,hora,motivo,id_paciente,id_medico):
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        self.hora = datetime.strptime(hora, "%H:%M").time()
        self.motivo = motivo
        self.id_paciente = id_paciente
        self.id_medico = id_medico

# crea una cita --> admin
# ver citas --> admin y medico
# actualizar citas --> admin y medico (solo estado, y cuando en la consulta anota la cita lo cambia a completado)
# eliminar citas --> admin

    def crear(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def citas():
        return Cita.query.all()
    
    @staticmethod
    def cita(id):
        return Cita.query.get(id)
    
    def actualizar(self,fecha=None,hora=None,motivo=None,estado=None,id_paciente=None,id_medico=None):
        if fecha:
            self.fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        if hora: 
            self.hora = datetime.strptime(hora, "%H:%M").time()
        if motivo:
            self.motivo = motivo
        if estado:
            self.estado = estado
        if id_paciente:
            self.id_paciente = id_paciente
        if id_medico:
            self.id_medico = id_medico
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def filtrar_citas(estado=None, id_paciente=None, id_medico=None):
        query = Cita.query
        
        if estado:
            query = query.filter_by(estado=estado)
        if id_paciente:
            query = query.filter_by(id_paciente=id_paciente)
        if id_medico:
            query = query.filter_by(id_medico=id_medico)
            
        return query.all()