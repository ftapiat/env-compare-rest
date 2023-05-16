import requests
from flask import Flask, url_for, request, json

from src.models.responses import AppResponse
from src.models.files import UploadedFiles
from src.models.file_types import FileTypeName, FileTypeFactory
from src.models.file_values import FileValues
from src.models.comparer import ComparedValues
from src.models.values import UploadedValues
from src.helpers import get_server_route
from src.requests import IsFileTypeRequest

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


@app.route("/compare/files", methods=["POST"])
def get_file_differences():
    # Todo Validate structure
    files = UploadedFiles(request.get_json()["files"])

    def make_file_request(file):
        return requests.post(get_server_route(url_for("get_file_values")), json={
            "file": file.serialized
        })

    file_1_response = make_file_request(files.file_1).json()
    file_1_values = FileValues.from_dict(file_1_response["data"])

    file_2_response = make_file_request(files.file_2).json()
    file_2_values = FileValues.from_dict(file_2_response["data"])

    def make_differences_request(values_file_1: FileValues, values_file_2: FileValues):
        return requests.post(get_server_route(url_for("get_value_differences")), json={
            "values": [
                values_file_1.serialized,
                values_file_2.serialized,
            ]
        })

    differences_response = make_differences_request(file_1_values, file_2_values).json()
    differences_value = differences_response["data"]

    return make_json_response({
        "values": {
            "file_1": file_1_values.serialized,
            "file_2": file_2_values.serialized
        },
        "differences": differences_value  # Already serialized
    })


@app.route("/file/values/get", methods=["POST"])
def get_file_values():
    # Todo Validate structure
    file = request.get_json()["file"]
    content = file["content"]
    file_name = file["name"]

    # Get file type
    get_type_request = requests.post(get_server_route(url_for("get_file_type")), json={
        "content": content
    })
    type_name = get_type_request.json()["data"]

    # try:
    values = FileTypeFactory.from_type(FileTypeName(type_name), content).get_values(file_name)
    return make_json_response(values.serialized)
# except Exception as e:
#     Todo Throw error
# return make_json_response(None)


@app.route("/file/type/get", methods=["POST"])
def get_file_type():
    # Todo Validate structure Has "content" key
    content = request.get_json()["content"]

    def make_is_type_request(type_name, file_content) -> bool:
        is_type_request = requests.post(get_server_route(url_for("is_file_type", type_name=type_name)), json={
            "content": file_content
        })
        return is_type_request.json()["data"]

    types_to_check = [
        FileTypeName.DOTENV.value,
        FileTypeName.OC_YAML_ENV_OBJ.value,
        FileTypeName.OC_YAML_ENV_LIST.value,
        FileTypeName.OC_YAML_CONFIGMAP.value
    ]

    for t in types_to_check:
        if make_is_type_request(t, content):
            return make_json_response(t)

    return make_json_response(FileTypeName.NONE.value)  # Todo error?


@app.route("/file/type/is/<type_name>", methods=["POST"])
def is_file_type(type_name):
    errors = IsFileTypeRequest().validate(request.get_json() | {"type_name": type_name})
    if errors:
        return make_json_response(False)  # Todo Throw error

    content = request.get_json()["content"]
    try:
        return make_json_response(FileTypeFactory.from_type(FileTypeName(type_name), content).is_valid())
    except Exception as e:
        # Todo Throw error
        return make_json_response(False)


@app.route("/compare/values", methods=["POST"])
def get_value_differences():
    # Todo Validate structure
    values = UploadedValues(request.get_json()["values"])
    differences = ComparedValues.from_files(values.file_1, values.file_2)
    return make_json_response(differences.serialized)
