import marshmallow
import requests
from flask import Flask, url_for, request

from src.models.responses import AppResponseStatus, AppResponseSchema, AppResponse
from src.models.comparable_files import ComparableFile
from src.models.file_types import FileTypeName, FileTypeFactory
from src.models.file_values import FileValues, FileValuesSchema
from src.models.comparer import ComparedValues, ComparedValuesSchema
from src.helpers import get_server_route
from src.requests import IsFileTypeRequest, GetFileTypeRequest, GetFileValuesRequest, GetFileValuesRequestSchema, \
    GetValueDifferencesRequestSchema, GetValueDifferencesRequest, GetFileDifferencesRequestSchema, \
    GetFileDifferencesRequest
from src.responses import GetFileValuesResponse, GetFileValuesResponseValues, GetFileValuesResponseSchema

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
    service = "get_file_differences"

    try:
        request_schema = GetFileDifferencesRequestSchema()
        get_file_differences_request: GetFileDifferencesRequest = request_schema.load(request.get_json())
    except marshmallow.ValidationError as err:
        return make_validation_json_response(err.messages, service)

    # Set file names default if not provided
    default_file_names = ["file_1", "file_2"]
    for i in range(len(get_file_differences_request.files)):
        if not get_file_differences_request.files[i].name:
            get_file_differences_request.files[i].name = default_file_names[i]

    # Get file values
    def make_file_values_request(file: ComparableFile) -> AppResponse[dict]:
        file_values_body = GetFileValuesRequestSchema().dump({"file": file})
        file_values_response = requests.post(get_server_route(url_for("get_file_values")), json=file_values_body)
        return AppResponseSchema().load(file_values_response.json())

    file_values_schema = FileValuesSchema()
    file_1_values = file_values_schema.load(make_file_values_request(get_file_differences_request.file_1).data)
    file_2_values = file_values_schema.load(make_file_values_request(get_file_differences_request.file_2).data)

    # Get differences between the file values
    def make_differences_request(values_file_1: FileValues, values_file_2: FileValues) -> AppResponse:
        differences_body = GetValueDifferencesRequestSchema() \
            .dump(GetValueDifferencesRequest([values_file_1, values_file_2]))
        differences_response = requests.post(get_server_route(url_for("get_value_differences")), json=differences_body)
        return AppResponseSchema().load(differences_response.json())

    differences = make_differences_request(file_1_values, file_2_values)
    differences_schema = ComparedValuesSchema()
    differences_value: ComparedValues = differences_schema.load(differences.data)

    # Make response
    file_values = GetFileValuesResponseValues(file_1_values, file_2_values)
    response = GetFileValuesResponse(file_values, differences_value)
    message = "Successfully compared files"
    return make_json_response(GetFileValuesResponseSchema().dump(response), message=message, service=service)


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
    get_type_response: AppResponse[str] = AppResponseSchema().load(get_type_request.json())
    if get_type_response.status.value is AppResponseStatus.ERROR.value:
        return AppResponseSchema().dump(get_type_response), get_type_request.status_code

    type_name = get_type_response.data
    values = FileTypeFactory.from_type(FileTypeName(type_name), file.content).get_values(file.name)
    message = "File values retrieved successfully"
    return make_json_response(FileValuesSchema().dump(values), message=message, service=service)


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
        is_type_response: AppResponse[bool] = AppResponseSchema().load(is_type_request.json())
        if is_type_response.status.value is AppResponseStatus.ERROR.value:
            return False

        return is_type_response.data

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
    print(type_name, is_valid)

    # Checks the article to use in the response
    vowels = ('a', 'e', 'i', 'o', 'u')  # No need to check for uppercase
    starts_with_vowel = type_name[0].lower() in vowels
    article = "an" if starts_with_vowel else "a"

    # Message depending on the file if it's valid or not
    message = f"The file is {article if is_valid else f'not {article}'} {type_name}"
    return make_json_response(is_valid, message=message, service=service)


@app.route("/compare/values", methods=["POST"])
def get_value_differences():
    service = "get_value_differences"

    try:
        values: GetValueDifferencesRequest = GetValueDifferencesRequestSchema().load(request.get_json())
    except marshmallow.ValidationError as err:
        return make_validation_json_response(err.messages, service)

    differences = ComparedValues.from_files(values.file_1, values.file_2)
    message = "Successfully compared values"
    return make_json_response(ComparedValuesSchema().dump(differences), message=message, service=service)
