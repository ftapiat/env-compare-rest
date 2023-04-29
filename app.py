import requests
from flask import Flask, url_for, request
from src.models.files import UploadedFiles
from src.helpers import get_server_route, obj_to_json


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    res = requests.get(get_server_route(url_for("print_hi", name="random user!")))
    return res.text

@app.route("/hi/<name>", methods=["GET"])
def print_hi(name):
    return f"Hi, {name}"

@app.route("/compare-files", methods=["POST"])
def compare_files():
    # Todo Validate structure
    files = UploadedFiles(request.get_json()["files"])

    def make_file_request(file):
        return requests.post(get_server_route(url_for("get_file_values")), json={
            "file": obj_to_json(file)
        })

    res_file_1 = make_file_request(files.file_1)
    # return obj_to_json(res_file_1)
    return res_file_1.json()
    # Todo file 2
    # Todo compare files
    # Todo return result

@app.route("/file-values", methods=["POST"])
def get_file_values():
    # Todo Validate structure
    file = request.get_json()["file"]
    # Todo get type of file and get values
    return obj_to_json(file)