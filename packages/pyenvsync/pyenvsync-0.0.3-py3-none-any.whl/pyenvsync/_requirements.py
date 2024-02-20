from ._ouput import warning, error


def compare_requirements(requirements: dict) -> bool:
    matching = True
    for package, version in requirements.items():
        try:
            installed_version = __import__(package).__version__
            if version is not None and installed_version != version:
                matching = False
                message = f"Mismatching version of the '{package}' package. "
                message += f"Expected '{version}', but found '{installed_version}'."
                warning(message)

        except ImportError:
            matching = False
            if version is not None:
                error(f"The '{package}' package is not installed. Expected version '{version}'.")
            else:
                error(f"The '{package}' package is not installed.")

        except Exception:
            error(f"An error occurred while checking the '{package}' package.")

    return matching
