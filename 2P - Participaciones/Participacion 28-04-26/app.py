from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def init_db():
    with app.app_context():
        db.create_all()
        print("base de datos creada")

class Producto(db.Model):
    __tablename__ = "productos"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    price = db.Column(db.Float,nullable=False)
    stock = db.Column(db.Integer,default=0)

    def __repr__(self):
        return f"producto('{self.name}','{self.price}','{self.stock}')"

# --- OPERACIONES CRUD ---

def create_product():
    with app.app_context():
        producto1 = Producto(name="Arroz 1kg",price=8.50,stock=120)
        producto2 = Producto(name="Aceite Vegetal 1L",price=15.00,stock=80)
        producto3 = Producto(name="Azúcar 1kg",price=7.00,stock=95)
        producto4 = Producto(name="Leche Entera 1L",price=6.50,stock=150)
        producto5 = Producto(name="Pan de Molde",price=10.00,stock=60)
        producto6 = Producto(name="Huevos (docena)",price=18.00,stock=70)
        producto7 = Producto(name="Fideos 500g",price=5.00,stock=110)
        producto8 = Producto(name="Galletas Surtidas",price=12.00,stock=50)
        producto9 = Producto(name="Refresco 2L",price=11.50,stock=90)
        producto10 = Producto(name="Café Molido 250g",price=22.00,stock=40)

        db.session.add(producto1)
        db.session.add(producto2)
        db.session.add(producto3)
        db.session.add(producto4)
        db.session.add(producto5)
        db.session.add(producto6)
        db.session.add(producto7)
        db.session.add(producto8)
        db.session.add(producto9)
        db.session.add(producto10)

        db.session.commit()
        print("Datos guardados")

# Read 
def read_product():
    with app.app_context():
        productos = Producto.query.all()
        if productos:
            print("Productos registrados:")
            for producto in productos:
                print(producto)
        else:
            print("No se encontraron productos registrados")

        filtrados = Producto.query.filter(Producto.price>10.00).all()
        if filtrados:
            print("Productos con precio mayores a 10: ")
            for filtrado in filtrados:
                print(filtrado)
        else:
            print("No se encontraron productos con precio mayor a 10")
        
        producto = Producto.query.filter_by(stock=50).first()
        if producto:
            print("Producto con stock de 50")
            print(producto)
        else:
            print("No se encontró el producto son stock de 50")
        
# Update
def update_product():
    with app.app_context():
        producto = Producto.query.filter_by(stock=50).first()
        if producto:
            producto.stock = 0
            db.session.commit()
            print("Producto actualizado")
        else:
            print("no se encontró el producto con stock de 50")

# Delete
def delete_product():
    with app.app_context():
        producto = Producto.query.filter_by(id=5).first()
        if producto:
            db.session.delete(producto)
            db.session.commit()
            print("Producto eliminado exitosamente")
        else:
            print("No se encontró el producto")

if __name__ == "__main__":
    init_db()
#    create_product()
    read_product()
    update_product()
    delete_product()