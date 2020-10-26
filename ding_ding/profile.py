from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import g

from .db import get_db
from .auth import login_required


bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def profile():
    return redirect(url_for('index'))
