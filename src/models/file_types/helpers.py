def get_list_values_from_yaml_content(yaml_content, object_key: str, expects_type: type):
    if isinstance(yaml_content, dict) and object_key in yaml_content:
        list_values = yaml_content[object_key]
    else:
        list_values = yaml_content

    if expects_type == dict and isinstance(list_values, dict) \
            or expects_type == list and isinstance(list_values, list):
        return list_values
    return None
