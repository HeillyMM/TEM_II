from database import db
from models.usuario_model import Usuario
from models.cita_model import Cita

class Medico(db.Model):
    __tablename__ = "medicos"

    id_medico = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(80),nullable=False)
    especialidad = db.Column(db.String(30),nullable=False)
    telefono = db.Column(db.String,nullable=False)
    correo = db.Column(db.String(100),nullable=False)

    usuario = db.relationship('Usuario',back_populates="medico",cascade="all,delete-orphan")
    consultas = db.relationship('Consulta',back_populates='medico')
    citas = db.relationship('Cita',back_populates='medico')

    def __init__(self,nombre,especialidad,telefono,correo):
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono
        self.correo = correo

    def guardar(self):
        usuario = Usuario(username=self.nombre,correo=self.correo,password=self.telefono+"_med",rol="medico",medico=self)
        db.session.add_all([self,usuario])
        db.session.commit()

    @staticmethod
    def medicos():
        return Medico.query.all()
    
    @staticmethod
    def medico(id):
        return Medico.query.get(id)
    
    def actualizar(self,nombre=None,especialidad=None,telefono=None,correo=None):
        if nombre:
            self.nombre = nombre
        if especialidad:
            self.especialidad = especialidad
        if telefono:
            self.telefono = telefono
        if correo:
            self.correo = correo

        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()