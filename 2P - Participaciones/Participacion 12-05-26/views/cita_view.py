from flask import render_template

# crea una cita --> admin
# ver citas --> admin y medico
# actualizar citas --> admin y medico (solo estado, y cuando en la consulta anota la cita lo cambia a completado)
# eliminar citas --> admin

def menu(citas, pacientes=None):
    return render_template('/citas/menu.html', citas=citas, pacientes=pacientes)

def crear(pacientes, medicos):
    return render_template('/citas/crear.html', pacientes=pacientes, medicos=medicos)

def actualizar(cita, pacientes, medicos):
    return render_template('/citas/actualizar.html', cita=cita, pacientes=pacientes, medicos=medicos)