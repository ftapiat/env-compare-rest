def openshift_list_has_valid_structure(values: list) -> bool:
    """
    Check if each value in list has the property "name"
    :param values:
    :return:
    """
    for value in values:
        if "name" not in value:
            return False

    return True


def openshift_get_values_from_list(values: list) -> list[dict[str, str]]:
    """
    Get the values from a list of objects.
    :param values:
    :return:
    """
    result = []
    for value in values:
        result.append(format_openshift_value_structure(value))
    return result


def format_openshift_value_structure(value: dict) -> dict[str, str]:
    if "value" not in value:
        value["value"] = ""
    else:
        value["value"] = str(value["value"])

    return {
        "key": value["name"],
        "value": value["value"]
    }
