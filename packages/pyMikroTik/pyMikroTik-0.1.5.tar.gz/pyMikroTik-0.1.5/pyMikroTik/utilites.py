from colorama import Fore, init
init(autoreset=True)


def print_color(text: str, color: str | None = None):
    COLORS = {
        'cyan': Fore.CYAN,
        'red': Fore.RED,
        'magenta': Fore.MAGENTA,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE
    }

    if not color:
        color = 'not_color'

    print(COLORS.get(color, Fore.RESET) + text)

