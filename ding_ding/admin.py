from flask import Blueprint
from flask import render_template

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def admin():
    return render_template('admin/admin.html')
