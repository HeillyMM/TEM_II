from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///helen.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String,nullable=False,unique=True)

    def __repr__ (self):
        return f"nombre = {self.nombre}"

def init_db():
    with app.app_context():
        db.create_all()
        print("base de datos creada")

def crear():
    with app.app_context():
        db.session.add(User(nombre = "helen keilly"))
        db.session.add(User(nombre = "limber limachi"))
        db.session.add(User(nombre = "kevin"))
        db.session.commit()
        print("Usuarios guardado")

def leer():
    with app.app_context():
        usuarios = User.query.all()
        for usuario in usuarios:
            print(usuario)

def actualizar():
    with app.app_context():
        usuario = User.query.filter_by(id=1).first()
        usuario.nombre = "Nayeli"
        db.session.commit()
        print("usuario actualizado")

def eliminar():
    with app.app_context():
        usuarios = User.query.filter((User.id==1)|(User.id==2)).all()
        for usuario in usuarios:
            db.session.delete(usuario)
        db.session.commit()
        print("usuario eliminado")


if __name__ == "__main__":
#    init_db()
#    crear()
    leer()
#    actualizar()
    eliminar()
    leer()