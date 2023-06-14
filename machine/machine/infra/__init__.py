import sqlite3

import click
from flask import current_app, g
from machine import resources
import importlib.resources as pkg_resources
import os
from machine.settings import MACHINE_NAME

def get_db():
    db = sqlite3.connect(f'{os.path.dirname(resources.__file__)}/data.db',
            detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db

def get_flask_db():
    if 'db' not in g:
        g.db = get_db()

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():

    db = sqlite3.connect(f'{os.path.dirname(resources.__file__)}/data.db',
        detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row

    inp_file = (pkg_resources.files(resources) / 'schema.sql')

    with inp_file.open("rt") as f:
        db.executescript(f.read())

    db_cursor = db.cursor()

    db_cursor.execute('INSERT INTO MACHINES(NAME)VALUES(?)', (MACHINE_NAME,))
    db.commit()
    db_cursor.close()
    db.close()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')