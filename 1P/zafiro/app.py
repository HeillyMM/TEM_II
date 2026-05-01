from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

def init_database():
    conn = sqlite3.connect("registro.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS notas(
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    nota NUMBER NOT NULL
    )
    """
    )
    conn.commit()
    conn.close()

init_database()


@app.route("/crear")
def crear():
    return render_template("crear.html")

@app.route("/registro",methods=['POST'])
def registro():
    conn = sqlite3.connect("registro.db")
    nombre = request.form['nombre']
    nota = request.form['nota']
    conn.execute(
        """INSERT INTO notas(nombre,nota) VALUES(?,?)""",(nombre,nota)
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/")
def index():
    conn = sqlite3.connect("registro.db")
    conn.row_factory=sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notas")
    lista = cursor.fetchall()
    return render_template("index.html",lista=lista)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = sqlite3.connect("registro.db")
    conn.execute("DELETE FROM notas WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/guardar_edicion/<int:id>",methods=['POST'])
def guardar_edicion(id):
    conn = sqlite3.connect("registro.db")
    nombre = request.form['nombre']
    nota = request.form['nota']
    conn.execute(
        """UPDATE notas SET nombre=?,nota=? WHERE id=?""",(nombre,nota,id)
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/editar/<int:id>")
def editar(id):
    conn = sqlite3.connect("registro.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notas WHERE id=?",(id,))
    nombre = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("editar.html",nombre=nombre)

if __name__ == "__main__":
    app.run(debug=True)