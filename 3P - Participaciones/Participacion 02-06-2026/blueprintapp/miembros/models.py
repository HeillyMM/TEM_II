#modelos que son parte de este modulo 
from blueprintapp.app import db
from flask_login import UserMixin

class Miembro(db.Model,UserMixin):
    __tablename__ = "miembros"

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    tipo = db.Column(db.Enum('admin','miembro'),nullable=False)

    tareas = db.relationship('Tarea',back_populates="miembro",cascade="all,delete-orphan")
    
    def __repr__(self):
        return f"<MIEMBRO: {self.nombre} - {self.email}>"