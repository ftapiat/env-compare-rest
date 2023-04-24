from flask import Flask, url_for
from config import *
import requests


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    ruta = url_for('print_hi', name='bienvenido!')
    res = requests.get(f'{ROOT_URL}{ruta}')
    return res.text


@app.route("/hi/<name>", methods=["GET"])
def print_hi(name):
    return f'Hola, {name}'