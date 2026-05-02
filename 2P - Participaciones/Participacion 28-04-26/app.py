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

class Product(db.Model):
    __tablename__ = "productos"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    price = db.Column(db.Float,nullable=False)
    stock = db.Column(db.Integer,nullable=False,default=0)

    def __repr__(self):
        return f"producto('{self.name}','{self.price}','{self.stock}')"

# --- OPERACIONES CRUD ---

def create_product(name,price,stock):
    with app.app_context():
        producto = Product(name=name,price=price,stock=stock)
        db.session.add(producto)
        db.session.commit()
        print("Producto registrado")

# Read 
def read_product(opcion):
    with app.app_context():
        if opcion == "1":
            productos = Product.query.all()
            if productos:
                print("Productos registrados:")
                for producto in productos:
                    print(f"Nombre: {producto.name} | Precio: {producto.price} | stock: {producto.stock}")
            else:
                print("No se encontraron productos registrados")
        elif opcion == "2":
            precio = input("Filtrar productos con precio mayor a: ")
            filtrados = Product.query.filter(Product.price>precio).all()
            if filtrados:
                print(f"Productos con precio mayores a {precio}: ")
                for filtrado in filtrados:
                    print(f"Nombre: {filtrado.name} | Precio: {filtrado.price} | stock: {filtrado.stock}")
            else:
                print(f"No se encontraron productos con precio mayor a {precio}")
        else:
            id = input("Id del producto a buscar: ")
            producto = Product.query.filter_by(id=id).first()
            if producto:
                print(f"Producto con id {id}:")
                print(f"nombre: {producto.name} | precio: {producto.price} | stock: {producto.stock}")
            else:
                print(f"No se encontró el producto con id {id}")
        
# Update
def update_product(id):
    with app.app_context():
        producto = Product.query.filter_by(id=id).first()
        if producto:
            print("1. Actualizar todo")
            print("2. Actualizar nombre")
            print("3. Actualizar precio")
            print("4. Actualizar stock")
            opcion = input("opcion elegida: ")
            if opcion == "1" or opcion == "2" or opcion == "3" or opcion == "4":
                if opcion == "1":
                    nombre = input("\nIngrese nuevo nombre: ")
                    precio = input("Ingrese nuevo precio: ")
                    stock = input("Ingrese nuevo stock: ")
                    producto.name = nombre
                    producto.price = precio
                    producto.stock = stock

                elif opcion == "2":
                    nombre = input("\nIngrese nuevo nombre: ")
                    producto.name = nombre

                elif opcion == "3":
                    precio = input("\nIngrese nuevo precio: ")
                    producto.price = precio

                else:
                    stock = input("\nIngrese nuevo stock: ")
                    producto.stock = stock
                
                db.session.commit()
                print("Producto actualizado")
            else:
                print("opción no válida")
        else:
            print(f"no se encontró el producto con id {id}")

# Delete
def delete_product(id):
    with app.app_context():
        producto = Product.query.filter_by(id=id).first()
        if producto:
            db.session.delete(producto)
            db.session.commit()
            print("Producto eliminado exitosamente")
        else:
            print(f"No se encontró el producto con id {id}")

if __name__ == "__main__":
    init_db()
    while True:
        print("\nMenú de Product: ")
        print("1. Registrar producto")
        print("2. Mostrar Productos registrados")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            nombre = input("\nNombre del producto: ")
            precio = input("Precio del producto: ")
            stock = input("Ingrese stock: ")
            if stock == "":
                stock = 0
            create_product(nombre,precio,stock)

        elif opcion == "2":
            print("\n1. Ver todos registros")
            print("2. ver productos segun precio")
            print("3. Ver información de producto específico")
            opcion = input("Elige una opción: ")
            if opcion == "1" or opcion =="2" or opcion =="3":
                read_product(opcion)
            else:
                print("opción no válida")

        elif opcion == "3":
            id = input("\nIngrese el id del producto: ")
            update_product(id)
            
        elif opcion == "4":
            id = input("\nIngrese el id del producto: ")
            delete_product(id)

        elif opcion == "5":
            break
        else:
            print("opción no válida")