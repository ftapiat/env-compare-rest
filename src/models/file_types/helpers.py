def get_list_values_from_yaml_content(yaml_content, object_key: str):
    list_values = None
    if isinstance(yaml_content, dict) and object_key in yaml_content:
        list_values = yaml_content[object_key]
    elif isinstance(yaml_content, list):
        list_values = yaml_content
    return list_values
