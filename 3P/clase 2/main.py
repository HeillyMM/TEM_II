from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# creaer base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///VIAJES.DB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Destino(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    destino = db.Column(db.String(50),nullable=False)
    pais = db.Column(db.String(50),nullable=False)
    valoracion = db.Column(db.Float,nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "destino": self.destino,
            "pais": self.pais,
            "valoracion": self.valoracion
        }
    
# Rutas 
@app.route("/")
def home():
    # Devolver una respuesta a traves de un mensaje {"menssage":"Bienvenido al sistema!!!..."}
    return jsonify(
        {"message":"Bienvenido al sistema!!!..."}
    )

# Obtiene lista de destinos en formato json 
# endpoint 1
@app.route("/destinos",methods=['GET'])
def get_destinos():
    destinos = Destino.query.all()
    return jsonify([destino.to_dict() for destino in destinos])

# usango get para encontrar solo 1 registro con id  - endpoint 2
@app.route("/destinos/<int:id>",methods=['GET'])
def get_destino(id):
    obj_destino = Destino.query.get(id)
    if obj_destino:
        return jsonify(obj_destino.to_dict())
    else:
        return jsonify({"error":"No existe el destino"}),400

# para agrregar un destino --> adicionar nuevos elementos -- endpoint 3
@app.route("/destinos",methods=['POST'])
def add_destino():
    data = request.get_json()

    objnew = Destino(destino=data["destino"],pais=data["pais"],valoracion=data["valoracion"])

    db.session.add(objnew)
    db.session.commit()
    return jsonify(objnew.to_dict()),201

# Actualizzación de un registro enviado mediante json con id
@app.route("/destinos/<int:id>",methods=['PUT'])
def update_destino(id):
    data = request.get_json()
    obj_destino = Destino.query.get(id)
    if obj_destino:
        obj_destino.destino = data.get("destino")
        obj_destino.pais = data.get("pais")
        obj_destino.valoracion = data.get("valoracion")

        db.session.commit()
        return jsonify(obj_destino.to_dict())

@app.route("/destinos/<int:id>",methods=['DELETE'])
def delete_destino(id):
    obj_destino = Destino.query.get(id)
    if obj_destino:
        db.session.delete(obj_destino)
        db.session.commit()
        return jsonify({"message":"Destino eliminado"})
    else:
        return jsonify({"error":"No existe el destino para eliminar"})


# inicio de la aplicación

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)