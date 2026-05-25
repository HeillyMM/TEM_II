from blueprintapp.app import db

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    precio = db.Column(db.Float,nullable=False)
    stock = db.Column(db.Integer,nullable=False)
    disponible = db.Column(db.Boolean,nullable=False)
    id_categoria = db.Column(db.Integer,db.ForeignKey('categorias.id'),nullable=False)

    categoria = db.relationship('Categoria',back_populates='productos')