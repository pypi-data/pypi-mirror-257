import sys


def version() -> str:
    try:
        sys_version = sys.version_info
        sys_version = f"{sys_version.major}.{sys_version.minor}.{sys_version.micro}"

    except Exception:
        raise Exception("Could not determine Python version.")

    return sys_version


def compare_versions(sys_version: str, config_version: str) -> bool:
    return sys_version == config_version
