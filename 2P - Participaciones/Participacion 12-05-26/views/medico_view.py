from flask import render_template


def menu(medicos):
    return render_template("medicos/menu.html",medicos=medicos)

# Formulario para agregar medico
def registrar_medico():
    return render_template("medicos/registrar_medico.html")

# Formulario para editar información de un médico
def editar_medico(medico):
    return render_template("medicos/editar_medico.html",medico=medico)
