import marshmallow
import requests
from flask import Flask, url_for, request

from src.models.responses import AppResponseStatus, AppResponseSchema
from src.models.files import UploadedFiles
from src.models.file_types import FileTypeName, FileTypeFactory
from src.models.file_values import FileValues, FileValuesSchema
from src.models.comparer import ComparedValues
from src.helpers import get_server_route
from src.requests import IsFileTypeRequest, GetFileTypeRequest, GetFileValuesRequest, GetFileValuesRequestSchema, \
    GetValueDifferencesRequestSchema, GetValueDifferencesRequest

app = Flask(__name__)


def make_validation_json_response(errors, service=None):
    message = "Validation error, please validate your request"
    validation_error_status_code = 422
    return make_json_response(errors, message, validation_error_status_code, service)


def make_json_response(data, message=None, status_code=200, service=None):
    schema = AppResponseSchema()
    app_response = schema.load({
        "data": data,
        "message": message,
        "status_code": status_code,
        "service": service
    })
    return schema.dump(app_response), status_code


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
    service = "get_file_values"
    request_schema = GetFileValuesRequestSchema()
    try:
        get_file_values_request: GetFileValuesRequest = request_schema.load(request.get_json())
    except marshmallow.ValidationError as err:
        return make_validation_json_response(err.messages, service)

    # Get file type
    file = get_file_values_request.file
    get_type_request_body: dict = GetFileTypeRequest(unknown=marshmallow.EXCLUDE).dump(file)
    get_type_request = requests.post(get_server_route(url_for("get_file_type")), json=get_type_request_body)
    get_type_response = AppResponseSchema().load(get_type_request.json())
    if get_type_response.status is AppResponseStatus.ERROR.value:
        return get_type_response, get_type_request.status_code

    type_name: str = get_type_response.data  # Todo Maybe change for generic Type
    values = FileTypeFactory.from_type(FileTypeName(type_name), file.content).get_values(file.name)
    return make_json_response(FileValuesSchema().dump(values), message="error_message", service=service)


@app.route("/file/type/get", methods=["POST"])
def get_file_type():
    service = "get_file_type"
    errors = GetFileTypeRequest().validate(request.get_json())
    if errors:
        return make_validation_json_response(errors, service=service)

    content = request.get_json()["content"]

    def make_is_type_request(type_name, file_content) -> bool:
        is_type_request = requests.post(get_server_route(url_for("is_file_type", type_name=type_name)), json={
            "content": file_content
        })
        return is_type_request.json()["data"]

    for t in FileTypeName.available_list():
        if make_is_type_request(t, content):
            message = f"File type is {t}"
            return make_json_response(t, message=message, service=service)

    # ERROR Because no type was found
    error_message = "Couldn't identify file type"
    return make_json_response(None, message=error_message, status_code=400, service=service)


@app.route("/file/type/is/<type_name>", methods=["POST"])
def is_file_type(type_name):
    service = "is_file_type"
    errors = IsFileTypeRequest().validate(request.get_json() | {"type_name": type_name})
    if errors:
        return make_validation_json_response(errors, service=service)

    content = request.get_json()["content"]
    is_valid = FileTypeFactory.from_type(FileTypeName(type_name), content).is_valid()

    # Checks the article to use in the response
    vowels = ('a', 'e', 'i', 'o', 'u')  # No need to check for uppercase
    starts_with_vowel = type_name[0].lower() in vowels
    article = "an" if starts_with_vowel else "a"

    # Message depending on the file if it's valid or not
    message = f"The file is {article if is_valid else f'not {article}'} {type_name}"
    return make_json_response(is_valid, message=message, service=service)


@app.route("/compare/values", methods=["POST"])
def get_value_differences():
    values: GetValueDifferencesRequest = GetValueDifferencesRequestSchema().load(request.get_json())
    differences = ComparedValues.from_files(values.file_1, values.file_2)
    return make_json_response(differences.serialized)
