from flask import Flask, url_for
import config
import requests


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    route = url_for('print_hi', name='random user!')
    full_route = f'{config.ROOT_URL}{route}'
    print(f"Calling route: {full_route}")
    res = requests.get(full_route)
    return res.text

@app.route("/hi/<name>", methods=["GET"])
def print_hi(name):
    return f'Hi, {name}'