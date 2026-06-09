# Llama a la aplicación y la hace funcionar
from blueprintapp.app import create_app

# se crea la aplicación con las caracteristicas y parámetros indicados en app.py
flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(debug=True)