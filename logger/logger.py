GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

def LogV1(msg: str) -> None:
    formatted_msg = f"{GREEN}[+]{RESET} {msg}"
    print(formatted_msg)

def LogV2(msg: str) -> None:
    formatted_msg = f"{RED}[-]{RESET} {msg}"
    print(formatted_msg)