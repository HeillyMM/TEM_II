from flask import Flask,redirect,url_for
from database import db
from controllers import medico_controller,usuario_controlller,paciente_controller,consulta_controller,cita_controller
from models.usuario_model import Usuario

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///clinica.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'clave_secreta_12345'

db.init_app(app)

app.register_blueprint(medico_controller.medico_bp)
app.register_blueprint(usuario_controlller.usuario_bp)
app.register_blueprint(paciente_controller.paciente_bp)
app.register_blueprint(consulta_controller.consulta_bp)
app.register_blueprint(cita_controller.cita_bp)

@app.route("/")
def home():
    return redirect(url_for('usuarios.login'))

if __name__ == "__main__":
#    with app.app_context():
#        db.create_all()
#        usuario = Usuario(username="admin",correo="admin@gmail.com",password="123",rol="admin")
#        usuario.guardar()
    app.run(debug=True)