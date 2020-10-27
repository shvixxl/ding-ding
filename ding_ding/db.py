import sqlite3
import click

from flask import current_app
from flask import Blueprint
from flask import jsonify
from flask import g

from flask.cli import with_appcontext

bp = Blueprint('db', __name__, url_prefix='/db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@bp.route('/stores/', defaults={'search': ''})
@bp.route('/stores/<search>')
def get_stores(search):
    stores = get_db().execute(
        'SELECT * FROM stores WHERE name LIKE ? ORDER BY name', ('%'+search+'%',)
    ).fetchall()
    stores = [dict(row) for row in stores]

    return jsonify(stores)


@bp.route('/items/', defaults={'search': ''})
@bp.route('/items/<search>')
def get_items(search):
    items = get_db().execute(
        'SELECT * FROM items WHERE name LIKE ? ORDER BY name', ('%'+search+'%',)
    ).fetchall()
    items = [dict(row) for row in items]

    return jsonify(items)
