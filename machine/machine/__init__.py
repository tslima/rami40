from flask import Flask, render_template
from machine.settings import MACHINE_NAME

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html', machine_name=MACHINE_NAME) 

    return app
