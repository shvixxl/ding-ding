from functools import wraps

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash
from flask import g

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from ding_ding.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Optional fields
        name = request.form['name']
        tel = request.form['tel']
        address = request.form['address']

        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'User with email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO users (email, password, tel, name, address) \
                VALUES (?, ?, ?, ?, ?)',
                (email, generate_password_hash(password), tel, name, address,)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        return render_template('auth/register.html', error=error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('profile.profile'))

        return render_template('auth/login.html', error=error)

    return render_template('auth/login.html')


@bp.route('/confirm', methods=['POST'])
@login_required
def confirm():
    password = request.form['password']

    if not check_password_hash(g.user['password'], password):
        return 'Wrong password', 403

    return '', 202


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
