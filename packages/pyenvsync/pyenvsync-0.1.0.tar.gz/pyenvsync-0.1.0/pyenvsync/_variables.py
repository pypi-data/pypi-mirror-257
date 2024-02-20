import os
from ._ouput import warning


def compare_variables(variables: dict) -> bool:
    matching = True
    for key, value in variables.items():
        if key not in os.environ:
            matching = False
            warning(f"The '{key}' environment variable is not set.\n\t\t Variable Description: {value}")

    return matching
