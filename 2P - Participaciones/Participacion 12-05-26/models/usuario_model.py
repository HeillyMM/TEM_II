from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    correo = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String,nullable=False)
    rol = db.Column(db.String,nullable=False)
    id_medico = db.Column(db.Integer,db.ForeignKey('medicos.id_medico'),nullable=True)

    medico = db.relationship('Medico',back_populates="usuario") 

    def __init__(self,username,correo,password,rol,medico=None):
        self.username = username
        self.correo = correo
        self.password = generate_password_hash(password)
        self.rol = rol
        self.medico = medico

    def verificar_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def login(username,password):
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.verificar_password(password):
                return usuario
        return None
    
    @staticmethod
    def usuarios():
        return Usuario.query.all()
    
    @staticmethod
    def usuario(id):
        return Usuario.query.get(id)

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self,username=None,correo=None,password=None):
        if username:
            self.username = username
        if correo:
            self.correo = correo
        if password:
            self.password = generate_password_hash(password)
        
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def usuario_medico(username):
        return Usuario.query.filter_by(username=username).first()