# Aunque conceptualmente Médicos y Pacientes tienen una relación Muchos a Muchos (N:M),
# NO se utiliza una tabla intermedia oculta (propiedad 'secondary="consultas"').
#
# La entidad 'Consulta' no es un simple puente de IDs; contiene atributos críticos
# del negocio (fecha, diagnóstico, tratamiento). En SQLAlchemy, usar 'secondary' 
# oculta la tabla intermedia e impide manipular estos campos extra de forma nativa.

from database import db

class Consulta(db.Model):
    __tablename__ = "consultas"
    
    id_consulta = db.Column(db.Integer,primary_key=True)
    fecha = db.Column(db.Date,nullable=False)
    diagnostico = db.Column(db.String(200),nullable=False)
    tratamiento = db.Column(db.String(200),nullable=False)
    id_medico = db.Column(db.Integer,db.ForeignKey('medicos.id_medico'))
    id_paciente = db.Column(db.Integer,db.ForeignKey('pacientes.id_paciente'))
    id_cita = db.Column(db.Integer, db.ForeignKey('citas.id_citas'), nullable=False, unique=True)

    medico = db.relationship('Medico',back_populates ="consultas")
    paciente = db.relationship('Paciente',back_populates ="consultas")
    cita = db.relationship('Cita', back_populates='consulta')

    def __init__(self,fecha,diagnostico,tratamiento,id_cita,id_paciente,id_medico):
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.id_cita = id_cita
        self.id_paciente = id_paciente
        self.id_medico = id_medico

# crear consulta -> medico
# editar consulta -> médico
# ver consulta -> medico y admin
# Eliminar consulta -> medico

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self,fecha,diagnostico,tratamiento,id_paciente,id_medico):
        if fecha:
            self.fecha = fecha
        if diagnostico:
            self.diagnostico = diagnostico
        if tratamiento:
            self.tratamiento = tratamiento
        if id_paciente:
            self.id_paciente = id_paciente
        if id_medico:
            self.id_medico = id_medico
        
        db.session.commit()

    @staticmethod
    def consultas():
        return Consulta.query.all()
    
    @staticmethod
    def consulta(id):
        return Consulta.query.get(id)
    
    @staticmethod
    def consulta_medico(id):
        return Consulta.query.filter_by(id_medico=id).all()
    
    @staticmethod
    def consulta_fecha(fecha):
        return Consulta.query.filter_by(fecha=fecha).all()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()