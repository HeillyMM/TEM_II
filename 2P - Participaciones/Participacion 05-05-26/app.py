from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///biblioteca.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Relaciones:
# Un libro es escrito por un solo autor (relación 1–N)
# Un libro puede pertenecer a varios géneros, y un genero puede tener varios libros (relación N–M)

# Tabla intermedia
libro_genero = db.Table(
    "libro_genero",
    db.Column("libro_id",db.Integer,db.ForeignKey("libros.id"),primary_key=True),
    db.Column("genero_id",db.Integer,db.ForeignKey("generos.id"),primary_key=True)
)

class Libro(db.Model):
    __tablename__ = "libros"
    id = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String(200),nullable=False)
    anio = db.Column(db.Integer)
    id_autor = db.Column(db.Integer,db.ForeignKey('autores.id'),nullable=False)

    autor = db.relationship('Autor',back_populates="libros")
    generos = db.relationship('Genero',secondary=libro_genero,back_populates="libros")

    def __repr__():
        return f"Titulo:"

class Autor(db.Model):
    __tablename__ = "autores"
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    nacionalidad = db.Column(db.String(100))

    libros = db.relationship('Libro',back_populates="autor",cascade="all,delete-orphan")

class Genero(db.Model):
    __tablename__ = "generos"

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50),nullable=False)

    libros = db.relationship('Libro',secondary=libro_genero,back_populates="generos",)

def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada correctamente!")

def insertar_datos():
    with app.app_context():

        # Autores
        autor1 = Autor(nombre="Gabriel García Márquez", nacionalidad="Colombia")
        autor2 = Autor(nombre="J.K. Rowling", nacionalidad="Reino Unido")
        autor3 = Autor(nombre="George Orwell", nacionalidad="Reino Unido")

        # Géneros
        genero1 = Genero(nombre="Realismo mágico")
        genero2 = Genero(nombre="Fantasía")
        genero3 = Genero(nombre="Distopía")
        genero4 = Genero(nombre="Novela")

        # Libros
        libro1 = Libro(titulo="Cien años de soledad", anio=1967, autor=autor1)
        libro2 = Libro(titulo="El amor en los tiempos del cólera", anio=1985, autor=autor1)

        libro3 = Libro(titulo="Harry Potter y el orden del fénix", anio=1997, autor=autor2)
        libro4 = Libro(titulo="Harry Potter y la cámara secreta", anio=1998, autor=autor2)

        libro5 = Libro(titulo="1984", anio=1949, autor=autor3)

        # Guardando relación N a M
        libro1.generos.extend([genero1, genero4])
        libro2.generos.extend([genero1, genero4])

        libro3.generos.extend([genero2, genero4])
        libro4.generos.extend([genero2, genero4])

        libro5.generos.extend([genero3, genero4])

        db.session.add_all([autor1, autor2, autor3, 
                            genero1, genero2, genero3, genero4, 
                            libro1, libro2, libro3, libro4, libro5])

        db.session.commit()
        print("Datos insertados correctamente")

def actualizar_datos():
    with app.app_context():
        print("\nActualizar el nombre del libro con id 2") #Harry potter y el orden del fénix
        libro = Libro.query.filter_by(id=2).first()
        if libro:
            libro.titulo = "Harry Portter y la cámara secreta"
            db.session.commit()
            print("Titulo del libro actualizado existosamente")
        else: 
            print("Libro no encontrado")

def eliminar_datos():
    with app.app_context():
        print("\n Eliminando autor con id 2") # J.K. rowling que tiene asociado 2 libros de harry potter
        autor = Autor.query.filter_by(id=2).first()
        if autor:
            db.session.delete(autor)
            db.session.commit()
            print("Autor Eliminado exitosamente")
        else:
            print("No se encontró el Autor")

if __name__ == "__main__":
#    init_db()
#    insertar_datos()
#    actualizar_datos()
    eliminar_datos()