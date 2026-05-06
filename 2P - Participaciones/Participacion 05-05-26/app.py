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

def insertar_datos(opcion):
    with app.app_context():
        if opcion == "1":
            print("\n Crear autor: ")
            nombre = input("Nombre del Autor: ")
            nacionalidad = input("Nacionalidad del Autor: ")
            autor = Autor(nombre=nombre, nacionalidad=nacionalidad)
            db.session.add(autor)
            db.session.commit()
            print("Autor agregado Existosamente")
        
        elif opcion == "2":
            print("Crear Libro: ")
            titulo = input("Titulo de Libro: ")
            anio = int(input("Año de publicación: "))
            id_autor = int(input("Id del Autor: "))
            autor = db.session.get(Autor,id_autor)
            if autor:
                libro = Libro(titulo=titulo,anio=anio,autor=autor)
                db.session.add(libro)
                cantidad_g = int(input("Cantidad de Géneros: "))
                if cantidad_g:
                    for i in range(cantidad_g):
                        id_genero = int(input("Id del género: "))
                        genero = db.session.get(Genero,id_genero)
                        if genero:
                            libro.generos.append(genero)
                        else:
                            print("Género no Encontrado")
                db.session.commit()
                print("Libro creado exitosamente")
            else:
                print("Autor no encontrado")
        
        elif opcion == "3":
            print("Creando Género")
            nombre = input("Nombre del género: ")
            genero = Genero(nombre=nombre)
            db.session.add(genero)
            db.session.commit()
            print("Género creado exitosamente")

def consultar_datos(opcion):
    with app.app_context():
        if opcion == "4":
        # Ver autores con sus libros
            print("\nAutores y libros publicados")
            autores = Autor.query.all()
            if autores:
                for autor in autores:
                    print(f"\n Autor: {autor.nombre}")
                    for libro in autor.libros:
                        print(f" - {libro.titulo}")
            else:
                print("No se encuentran Autores registrados")
        if opcion == "5":
        # Ver géneros con sus libros
            print("\nGéneros y Sus libros relacionados")
            generos = Genero.query.all()
            if generos:
                for genero in generos:
                    print(f"\nGénero: {genero.nombre}")
                    for libro in genero.libros:
                        print(f" - {libro.titulo}")
            else:
                print("No se encontraron géneros registrados")

def actualizar_datos():
    with app.app_context():
        print("\nActualizar el titulo del libro")
        id_libro = input("Ingrese el id del libro: ")
        libro = Libro.query.filter_by(id=id_libro).first() 
        if libro:
            libro.titulo = input("Nuevo titulo: ")
            db.session.commit()
            print("Titulo del libro actualizado existosamente")
        else: 
            print("Libro no encontrado")

def eliminar_datos():
    with app.app_context():
        print("\nEliminando Autor: ")
        id_autor = input("Ingrese el id del autor a eliminar: ")
        autor = Autor.query.filter_by(id=id_autor).first()
        if autor:
            db.session.delete(autor)
            db.session.commit()
            print("Autor Eliminado exitosamente")
        else:
            print("No se encontró el Autor")

if __name__ == "__main__":
    init_db()
    while True:
        print("\n --- MENÚ BIBLIOTECA ---")

        print("\nCREAR")
        print("1. Crear autor")
        print("2. Crear libro")
        print("3. Crear género")

        print("\nCONSULTAR")
        print("4. Ver autores con sus libros")
        print("5. Ver géneros con sus libros")

        print("\nACTUALIZAR")
        print("6. Actualizar título de libro")

        print("\nELIMINAR")
        print("7. Eliminar autor")

        print("\n0. SALIR")
        
        opcion = input("\nElegir un opción: ")
        
        if opcion == "1" or opcion == "2" or opcion == "3":
            insertar_datos(opcion)
        elif opcion == "4" or opcion == "5":
            consultar_datos(opcion)
        elif opcion == "6":
            actualizar_datos()
        elif opcion == "7":
            eliminar_datos()
        elif opcion == "0":
            break