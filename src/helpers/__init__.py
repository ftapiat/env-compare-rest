import config
import json


def get_server_route(route: str) -> str:
    full_route = f'{config.ROOT_URL}{route}'
    print(f"Calling route: {full_route}")
    return full_route


def obj_to_json(obj):
    return json.dumps(obj, default=lambda x: x.__dict__)
