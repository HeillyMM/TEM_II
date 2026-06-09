from flask import render_template,request,redirect,url_for,Blueprint,abort
from flask_login import login_required,current_user
from blueprintapp.app import db

bp_core = Blueprint('bp_core',__name__,template_folder="templates")

@bp_core.route("/")
@login_required
def index():
    if current_user.tipo != "admin":
        abort(403)
    return render_template('core/index.html')