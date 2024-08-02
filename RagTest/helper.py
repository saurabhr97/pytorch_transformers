class Colors:
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET_COLOR = "\033[0m"


def get_input():
    return input(Colors.GREEN + "User: " + Colors.RESET_COLOR)

def print_response(response):
    print(Colors.RED + "Assistant: " + Colors.RESET_COLOR, response)