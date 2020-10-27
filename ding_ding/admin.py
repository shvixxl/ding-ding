from functools import wraps

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import jsonify
from flask import g

from ding_ding.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
@admin_required
def admin():
    # Types of stores for sidebar menu
    types = get_db().execute(
        'SELECT DISTINCT type FROM stores ORDER BY type'
    ).fetchall()
    types = [type['type'] for type in types]

    return render_template('admin/admin.html', types=types)
