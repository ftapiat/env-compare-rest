import requests
from flask import Flask, url_for, request, json
from src.models.responses import AppResponse
from src.models.files import UploadedFiles
from src.models.file_types import FileTypeEnum, DotenvFileType
from src.helpers import get_server_route, obj_to_json

app = Flask(__name__)


def make_json_response(data):
    # Todo Update structure
    return json.jsonify(AppResponse(data).serialized)


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

    return make_json_response(files.serialized)

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


@app.route("/file/values/get", methods=["POST"])
def get_file_values():
    # Todo Validate structure
    file = request.get_json()["file"]
    content = file["content"]

    # Get file type
    get_type_request = requests.post(get_server_route(url_for("get_file_type")), json={
        "content": content
    })
    file_type = get_type_request.json()["data"]

    # Todo get values
    if file_type == FileTypeEnum.DOTENV.value:
        values = DotenvFileType(content).get_values()
    else:
        # Null
        # Todo Throw error
        values = None

    return make_json_response(values)


@app.route("/file/type/get", methods=["POST"])
def get_file_type():
    # Todo Validate structure Has "content" key
    content = request.get_json()["content"]

    def make_is_type_request(endpoint, file_content) -> bool:
        is_type_request = requests.post(get_server_route(url_for(endpoint)), json={
            "content": file_content
        })
        return is_type_request.json()["data"]

    is_dotenv = make_is_type_request("file_type_is_dotenv", content)

    if is_dotenv:
        file_type = FileTypeEnum.DOTENV
    else:
        # Todo add more file types
        file_type = FileTypeEnum.NONE

    return make_json_response(file_type.value)


@app.route("/file/type/is-dotenv", methods=["POST"])
def file_type_is_dotenv():
    # Todo Validate structure: Has "content" key
    content = request.get_json()["content"]
    return make_json_response(DotenvFileType(content).is_valid())
