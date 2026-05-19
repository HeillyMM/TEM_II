# rear paciente
# eliminar paciente
# actualizar paciente
# ver paciente

from database import db
from models.medico_model import Medico
from models.cita_model import Cita


class Paciente(db.Model):
    __tablename__ = "pacientes"

    id_paciente = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(30),nullable=False)
    edad = db.Column(db.Integer,nullable=False)
    direccion = db.Column(db.String,nullable=False)
    telefono = db.Column(db.String(30),nullable=False)

    consultas = db.relationship('Consulta',back_populates='paciente')
    citas = db.relationship('Cita',back_populates='paciente')


    def __init__(self,nombre,edad,direccion,telefono):
        self.nombre = nombre
        self.edad = edad
        self.direccion = direccion
        self.telefono = telefono
    
    def guardar(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def pacientes():
        return Paciente.query.all()
    
    @staticmethod
    def paciente(id):
        return Paciente.query.get(id)
    
    def consultas_paciente(self):
        return self.consultas
    
    def actualizar(self,nombre=None,edad=None,direccion=None,telefono=None):
        if nombre:
            self.nombre = nombre
        if edad:
            self.edad = edad
        if direccion:
            self.direccion = direccion
        if telefono:
            self.telefono = telefono
        
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()