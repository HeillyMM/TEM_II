from blueprintapp.app import db

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String,nullable=False)
    descripcion = db.Column(db.String(250),nullable=False)

    productos = db.relationship('Producto',back_populates='categoria',cascade="all,delete-orphan")