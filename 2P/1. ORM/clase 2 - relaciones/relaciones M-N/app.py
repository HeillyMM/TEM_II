# Para crear relaciones N a M tenemos 2 opciones:
# 1. Crear una clase por tabla
# 2. Crear las tablas (menos las muchos a muchos, esa sería una tabla intermedia sin modelo) 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///school.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición de modelos n a m (escenario 2)

# Tabla intermedia sin modelos asociados
student_course = db.Table(
    "student_course",
    db.Column("student_id",db.Integer,db.ForeignKey("students.id"),primary_key=True),
    db.Column("course_id",db.Integer,db.ForeignKey("courses.id"),primary_key=True)
)

class Student(db.Model):    
    __tablename__ = "students"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)

    # Parámetro que permite relacionar con tabla intermedia
    courses = db.relationship("Course",secondary=student_course,back_populates="students")

    def __repr__(self):
        return f"<Estudiante: {self.name}>"
    
class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)

    students = db.relationship("Student",secondary=student_course,back_populates="courses")

    def __repr__(self):
        return f"<Curso:  titulo = {self.title}>"

def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente")

# Insertar datos
def insert_datos():
    with app.app_context():
        # Crear estudiantes
        s1 = Student(name = "Helen Keilly")
        s2 = Student(name = "Juan Mamani")
        s3 = Student(name = "Erika Mollinedo")
        # Crear cursos
        c1 = Course(title = "Programación con Python")
        c2 = Course(title = "JavaScript")
        c3 = Course(title = "React")        

        # Inscribiendo alumnos a los cursos
        s1.courses.extend([c1,c2]) # más de uno
        s2.courses.append(c2) # inscribiendo a uno solo
        s3.courses.extend([c2,c3])

        db.session.add_all([s1,s2,s3,c1,c2,c3])
        db.session.commit()
        print("Estudiantes y cursos insertados correctamente")

def query_data():
    with app.app_context():
        print("\nListado de Estudiantes y cursos: ")
        students = Student.query.all()
        if students:
            for student in students:
                print(f"\n {student.name} está inscrito en:")
                for course in student.courses:
                    print(f" - {course.title}")
        else:
            print("No hay estudiantes registrados")
        
        print("\nListado de cursos y estudiantes que están inscritos")
        courses = Course.query.all()
        if courses:
            for course in courses:
                print(f"\nCurso: {course.title}")
                print("Estudiantes:")
                for estudiante in course.students:
                    print(f"- {estudiante.name}")

def update_relations():
    with app.app_context():
        print("Agregar un estudiante a un curso: ")
        student = Student.query.filter_by(id=2).first()
        course = Course.query.filter_by(id=1).first()
        if student and course:
            student.courses.append(course)
            db.session.commit()
            print("Inscripción actualizada")
        else:
            print("Estudiante o curso no encontrado")

def delete_relation():
    with app.app_context():
        print("\nEliminación de la inscripción en un curso")
        student = Student.query.filter_by(id=1).first()
        course = Course.query.filter_by(id=1).first()
        if student and course:
            student.courses.remove(course)
            db.session.commit()
            print("Se eliminó la inscripción")
        else:
            print("No se encontró estudiante o curso.")

if __name__ == "__main__":
#    init_db()
#    insert_datos()
#    update_relations()
    delete_relation()
    query_data()