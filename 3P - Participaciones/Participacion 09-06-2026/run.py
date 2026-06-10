from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///peliculas.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Pelicula(db.Model):
    __tablename__ = "peliculas"
    
    id = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String(50),nullable=False)
    genero = db.Column(db.String(20),nullable=False)
    calificacion = db.Column(db.Float,nullable=False)

    def to_dict(self):
        return {
            "id":self.id,
            "titulo":self.titulo,
            "genero":self.genero,
            "calificacion":self.calificacion
        }

# 1er endpoint: Obtener todas las peliculas
@app.route("/peliculas",methods=['GET'])
def peliculas():
    peliculas = Pelicula.query.all()
    return jsonify([pelicula.to_dict() for pelicula in peliculas])

# 2do endpoint: Obtener una pelicula en específico enviando su id
@app.route("/peliculas/<int:id>",methods=['GET'])
def pelicula(id):
    pelicula = Pelicula.query.get(id)
    if pelicula:
        return jsonify(pelicula.to_dict())
    else:
        return jsonify({"message":"No se encontró la pelicula"})

# 3er endpoint: Insertar una pelicula en la base de datos
@app.route("/peliculas",methods=['POST'])
def crear_pelicula():
    try:
        pelicula_f = request.get_json()
        pelicula = Pelicula(
            titulo=pelicula_f["titulo"],
            genero=pelicula_f["genero"],
            calificacion=pelicula_f["calificacion"]
            )
        db.session.add(pelicula)
        db.session.commit()
        return jsonify(pelicula.to_dict()),201
    except KeyError:
        return jsonify({"message":"no se enviaron todos los campos"}),400
    
# 4to endpoint: Editar datos de una pelicula enviando su id
@app.route("/peliculas/<int:id>",methods=['PUT'])
def editar_pelicula(id):
    pelicula = Pelicula.query.get(id)
    if pelicula:
        pelicula_f = request.get_json()
        pelicula.titulo = pelicula_f.get("titulo", pelicula.titulo)
        pelicula.genero = pelicula_f.get("genero", pelicula.genero)
        pelicula.calificacion = pelicula_f.get("calificacion", pelicula.calificacion)

        db.session.commit()
        return jsonify(pelicula.to_dict())
    else:
        return jsonify({"message":"No se encontró la pelicula"})
        
# 5to endpoint: Eliminar pelicula enviando su id
@app.route("/peliculas/<int:id>",methods=['DELETE'])
def eliminar_pelicula(id):
    pelicula = Pelicula.query.get(id)
    if pelicula:
        db.session.delete(pelicula)
        db.session.commit()
        return jsonify({"message":"La pelicula fue eliminada"})
    else:
        return jsonify({"message":"No se encontró la pelicula"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)