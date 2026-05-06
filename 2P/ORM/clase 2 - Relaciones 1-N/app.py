from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False)

    # campo especial Para ver a partir de usuarios que post tiene agregado
    posts = db.relationship('Post',back_populates='user',cascade = "all, delete-orphan")
    # cascade -> Parámetro que nos permite eliminar inclusive elementos relacionados

    def __repr__(self):
        return f"\nUsuario: {self.name} | Email: {self.email})"
    
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    #Llave foránea
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    # campo que sirve para reconocer quien es el dueño de ese post
    user = db.relationship('User',back_populates="posts")

    def __repr__(self):
        return f"POST: \ntitle: {self.title} User: {self.user.name} - {self.user.email}"
    
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente")

# Operaciones CRUD
def insert_data():
    with app.app_context():
        user1 = User(name = "Helen Keilly",email = "heilly.other@gmail.com")
        user2 = User(name = "Kevin Mamani",email = "kevinmolli@gmail.com")
        user3 = User(name = "Limber Limachi",email = "limlimachi@gmail.com")
        
        post1 = Post(title = "Primer post de Helen ", 
                    content = "Primera publicación", 
                    user = user1)
        post2 = Post(title = "Segundo post de Helen ", 
                    content = "Primera publicación", 
                    user = user1)
        post3 = Post(title = "Primer post de Kevin ", 
                    content = "Entrada uno de Kevin", 
                    user = user2)
        post4 = Post(title = "Primer post de Limber ", 
                    content = "Entrada uno de Limber", 
                    user = user3)
        
        db.session.add_all([user1,user2,user3,post1,post2,post3,post4])
        db.session.commit()
        print("Usuarios y entradas insertadas")

def query_data():
    with app.app_context():
        print("\nListado de Usuarios y sus publicaciones")
        # Obtener todos los registros
        users = User.query.all()
        for user in users:
            print(user)

            for post in user.posts:
                print(post)

def update_data():
    with app.app_context():
        # Actualizar post
        print("\nActualizando una publicación")
        post = Post.query.filter_by(id=2).first()
        if post:
            post.content = "Entrada Actualizada de Helen"
            db.session.commit()
            print("\nEntrada actualizada existosamente")
        else:
            print("No se encontró el usuario")

def delete_data():
    # Eliminar un usuario y sus posts
    with app.app_context():
        print("\nEliminar usuarios en cascada: ")
        user = User.query.filter_by(id=1).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print("Usuario eliminado con éxito")
        else:
            print("Usuario no encontrado")

if __name__ == "__main__":
#    init_db()
#    insert_data()
#    update_data()
    delete_data()
    query_data()