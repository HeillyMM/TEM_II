from flask import render_template

def menu(pacientes):
    return render_template('pacientes/menu.html',pacientes=pacientes)

def actualizar(paciente):
    return render_template('pacientes/actualizar.html',paciente=paciente)

def crear():
    return render_template('/pacientes/crear.html')

def consultas(consultas):
    return render_template('/pacientes/consultas.html',consultas=consultas)