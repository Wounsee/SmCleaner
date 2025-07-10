import os
import subprocess
import ctypes
import platform
from colorama import Fore, Style


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def get_color(value, thresholds):
    if value < thresholds[0]:
        return Fore.GREEN
    elif value < thresholds[1]:
        return Fore.YELLOW
    else:
        return Fore.RED


def print_section(title, color="white"):
    colors = {
        "red": Fore.RED + Style.BRIGHT,
        "green": Fore.GREEN + Style.BRIGHT,
        "yellow": Fore.YELLOW + Style.BRIGHT,
        "blue": Fore.BLUE + Style.BRIGHT,
        "magenta": Fore.MAGENTA + Style.BRIGHT,
        "cyan": Fore.CYAN + Style.BRIGHT,
        "white": Fore.WHITE + Style.BRIGHT
    }
    color_code = colors.get(color.lower(), Fore.WHITE + Style.BRIGHT)
    width = 80
    print(f"\n{color_code}{'=' * width}")
    print(f"{title.center(width)}")
    print(f"{'=' * width}{Style.RESET_ALL}\n")


def run_as_admin():
    if platform.system() != "Windows":
        return True

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def print_progress_bar(percentage, length=20):
    blocks = int(percentage / 100 * length)
    bar = "█" * blocks + "-" * (length - blocks)
    color = get_color(percentage, [70, 90])
    return f"{color}[{bar}]"


def get_choice(min_val, max_val):
    while True:
        try:
            choice = int(input(f">>> {Style.RESET_ALL}"))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"{Fore.RED}Пожалуйста, введите число от {min_val} до {max_val}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Ошибка: введите целое число{Style.RESET_ALL}")