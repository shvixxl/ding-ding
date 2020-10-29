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
    types = get_db().execute(
        'SELECT DISTINCT type FROM stores ORDER BY type'
    ).fetchall()
    types = [type['type'] for type in types]

    return render_template('admin/admin.html', types=types)


@bp.route('/panel/')
@admin_required
def admin_panel():
    search = request.args.get('q', default='')

    db = get_db()

    types = db.execute(
        'SELECT DISTINCT type FROM stores ORDER BY type'
    ).fetchall()
    types = [type['type'] for type in types]

    stores = get_db().execute(
        'SELECT * FROM stores WHERE name LIKE ? ORDER BY name', ('%'+search+'%',)
    ).fetchall()
    types = [{'name': t, 'count': len([s for s in stores if s['type'] == t])} for t in types]

    return render_template('admin/panel.html', types=types, stores=stores)


@bp.route('/store/<int:store_id>')
@admin_required
def store(store_id):
    store = get_db().execute(
        'SELECT * FROM stores WHERE id = ? ORDER BY name', (store_id,)
    ).fetchone()

    items = get_db().execute(
        'SELECT * FROM items WHERE store_id = ? ORDER BY name', (store_id,)
    ).fetchall()

    # Types of stores for sidebar menu
    types = get_db().execute(
        'SELECT DISTINCT type FROM stores ORDER BY type'
    ).fetchall()
    types = [type['type'] for type in types]

    return render_template('admin/store.html', store=store, items=items, types=types)


@bp.route('/add_item/', methods=['POST'])
@admin_required
def add_item():
    store_id = request.form['store-id']

    name = request.form['name']
    price = request.form['price']
    img = request.form['img']
    description = request.form['description']

    db = get_db()
    error = None

    if not store_id:
        error = 'Unknown error. Try to reload page.'
    elif not name:
        error = 'Name is not provided.'
    elif not price:
        error = 'Price is not provided.'

    if error is not None:
        return jsonify(error=error), 400

    db.execute(
        'INSERT INTO items (store_id, name, price, img, description) \
         VALUES (?, ?, ?, ?, ?)',
         (store_id, name, price, img, description,)
    )
    db.commit()

    return '', 200


@bp.route('/edit_item/', methods=['POST'])
@admin_required
def edit_item():
    item_id = request.form['item-id']

    name = request.form['name']
    price = request.form['price']
    img = request.form['img']
    description = request.form['description']

    db = get_db()
    error = None

    if not item_id:
        error = 'Unknown error. Try to reload page.'
    elif not name:
        error = 'Name is not provided.'
    elif not price:
        error = 'Price is not provided.'

    if error is not None:
        return jsonify(error=error), 400

    db.execute(
        'UPDATE items \
         SET name = ?, price = ?, img = ?, description = ? \
         WHERE id = ?',
         (name, price, img, description, item_id,)
    )
    db.commit()

    return '', 200


@bp.route('/delete_item/', methods=['POST'])
@admin_required
def delete_item():
    item_id = request.form['item-id']

    db = get_db()
    error = None

    if not item_id:
        error = 'Unknown error. Try to reload page.'

    if error is not None:
        return jsonify(error=error), 400

    db.execute(
        'DELETE FROM items WHERE id = ?', (item_id,)
    )
    db.commit()

    return '', 200


@bp.route('/add_store/', methods=['POST'])
@admin_required
def add_store():
    name = request.form['name']
    type = request.form['type']
    img = request.form['img']
    description = request.form['description']

    db = get_db()
    error = None

    if not name:
        error = 'Name is not provided.'
    elif not type:
        error = "Type is not provided."

    if error is not None:
        return jsonify(error=error), 400

    db.execute(
        'INSERT INTO stores (name, type, img, description) \
         VALUES (?, ?, ?, ?)',
         (name, type, img, description,)
    )
    db.commit()

    return '', 200


@bp.route('/edit_store/', methods=['POST'])
@admin_required
def edit_store():
    store_id = request.form['store-id']

    name = request.form['name']
    type = request.form['type']
    img = request.form['img']
    description = request.form['description']

    db = get_db()
    error = None

    if not id:
        error = 'Unknown error. Try to reload page.'
    elif not name:
        error = 'Name is not provided.'
    elif not type:
        error = "Type is not provided."

    if error is not None:
        return jsonify(error=error), 400

    db.execute(
        'UPDATE stores \
         SET name = ?, type = ?, img = ?, description = ? \
         WHERE id = ?',
         (name, type, img, description, store_id,)
    )
    db.commit()

    return '', 200


@bp.route('/delete_store/', methods=['POST'])
@admin_required
def delete_store():
    store_id = request.form['store-id']

    db = get_db()
    error = None

    if not store_id:
        error = 'Unknown error. Try to reload page.'

    if error is not None:
        return jsonify(error=error), 400

    db.execute(
        'DELETE FROM stores WHERE id = ?', (store_id,)
    )
    db.commit()

    return '', 200
