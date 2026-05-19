# crear consulta -> medico
# editar consulta -> médico
# ver consulta -> medico y admin
# Eliminar consulta -> medico
from flask import render_template

def crear(pacientes,citas_disponibles):
    return render_template('/consultas/crear.html',pacientes=pacientes,citas=citas_disponibles)

def actualizar(consulta,pacientes):
    return render_template('/consultas/actualizar.html',consulta=consulta,pacientes=pacientes)

def menu(consultas):
    return render_template('/consultas/menu.html',consultas=consultas)
