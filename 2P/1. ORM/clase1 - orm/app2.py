# VIDEO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tutorial.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo
class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False,unique=True)

    def __repr__(self):
        return f"user(name='{self.name}',email='{self.email}')"
    
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente")

# Operaciones CRUD
# Create
def insert_user():
    with app.app_context():
        # Instanciación de objetos tipo user
        user1 = Users(name="Bruno Diaz",email="bruno@gmail.com")
        user2 = Users(name="Ricardo Tapia",email="ricky@gmail.com")
        user3 = Users(name="Zacarias FLores",email="zaca@gmail.com")

        #Adición de objetos (registro en la tabla)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        # Consolida los cambios en la base de datos
        db.session.commit()
        print("Datos insertados")

# Read
def query_users():
    with app.app_context():
        # Consultas todos los registros de los usuarios
        print("Listado de usuarios")
        usuarios = Users.query.all()
        for item in usuarios:
            print(item)

        # Consultas que cubren ciertas condiciones
        print("Listado de registros filtrados")
        filtrado = Users.query.filter(Users.id>1).all()
        for item in filtrado:
            print(item)

        # Consulta de un solo usuario
        usuario = Users.query.filter_by(id=5).first()
        if usuario:
            print("Usuario filtrado: ",usuario)
        else:
            print("Usuario no encontrado")

# Update
def update_user():
    with app.app_context():
        print("Actualización de un registro")
        usuario = Users.query.filter_by(id=1).first()
        if usuario:
            usuario.name = "Helen Keilly"
            usuario.email = "heilly.other@gmail.com"
            # COnsolida los cambios de la base de datos
            db.session.commit()
            print("Usuario actualizado", usuario)
        else:
            print("usuario no encontrado")

# Delete
def delete_user():
    with app.app_context():
        print("ELiminación de registros")
        usuario = Users.query.filter_by(id=3).first()
        if usuario:
            db.session.delete(usuario)
            # Consolida los cambios de la base de datos
            db.session.commit()
            print("Usuario eliminado satisfactoriamente")
        else:
            print("Usuario no encontrado")

if __name__  == "__main__":
    init_db()
#    insert_user()
    query_users()
    update_user()
    delete_user()