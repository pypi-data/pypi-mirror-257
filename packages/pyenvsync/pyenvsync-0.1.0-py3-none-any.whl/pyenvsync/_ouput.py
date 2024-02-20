def error(message: str) -> None:
    print(f"\033[91mERROR\t\t\033[0m {message}")


def warning(message: str) -> None:
    print(f"\033[93mWARNING\t\t\033[0m {message}")


def success(message: str) -> None:
    print(f"\033[92mSUCCESS\t\t\033[0m {message}")


def step(message: str, linebreak: bool = True) -> None:
    border = '-' * len(message)
    if linebreak:
        print(f"\n{border}\n{message}\n{border}")
    else:
        print(f"{border}\n{message}\n{border}")
