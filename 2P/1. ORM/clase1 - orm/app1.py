# DIAPOSITIVA
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///almacen.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Creando tablas ---
# clase que representa una tabla de base de datos
class User(db.Model):
    #nombre de la tabla
    __tablename__="users"
    #definimos columnas
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False,unique=True)

    #Representación del objeto en texto -- sirve para ver la base de datos
    def __repr__(self):
        return f"User('{self.name}','{self.email}')"

#crea fisicamente la base de datos
def init_db():
    with app.app_context():
        db.create_all()
        print("Tablas creadas exitosamente")

# --- CRUD ---

# Create
def insert_users():
    with app.app_context():
        # Insertamos filas
        user1 = User(name="Helen Keilly",email="heilly.other@gmail.com")
        user2 = User(name="Limber",email="limachilimber@gmail.com")

        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()
        print("usuarios insertados")

# Read
def query_users():
    with app.app_context():
        # Seleccionar todos
        todos = User.query.all()
        # Con filtro 
        filtrados = User.query.filter(User.id>=1).all()
        # Un solo registro
        usuario = User.query.filter_by(id=1).first()

        if usuario:
            print(usuario)

# Update
def update_user():
    with app.app_context():
        user = User.query.filter_by(id=1).first()

        if user:
            user.name = "Kevin"
            user.email = "kevinmollinedo@gmail.com"
            db.session.commit()

            print("usuario actulizado")

# Delete
def delete_user():
    with app.app_context():
        user = User.query.filter_by(id=3).first()

        if user:
            db.session.delete(user)
            db.session.commit()

            print("Usuario eliminado")

if __name__ == "__main__":
    init_db()
    insert_users()
    query_users()
    update_user()
    delete_user()

    app.run(debug=True)