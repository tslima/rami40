from flask import Flask, render_template
from machine.settings import MACHINE_NAME
from machine.communication import start_receive
from machine.infra import close_db, init_db_command
import sys

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



def create_app():

    if sys.argv[1] == 'run':
        start_receive()

    app = Flask(__name__)
    init_app(app)

    @app.route('/')
    def home():
        return render_template('index.html', machine_name=MACHINE_NAME) 

    return app
