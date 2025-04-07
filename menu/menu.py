import os
import re
from colorama import Fore, Back, Style

from utils.beautiful_print import header


def get_menu_choice(options):
    shortcuts = scan_short_cuts(options)
    selected_index = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        show_menu(options, selected_index)

        key = b'\a'
        try:
            import msvcrt
            char = msvcrt.getch()
        except:
            pass

        if key == b'\x1b':
            return -1
        elif key == b'\r':
            return selected_index
        elif key in (b'\x48', b'\x50'):
            selected_index = (selected_index + (1 if key == b'\x50' else -1) + len(options)) % len(options)
        elif key in shortcuts:  # Shortcut key
            return shortcuts[key]
        elif key == b'\a':
            print('error , may not support your system')
            exit()


# endregion
def get_key():  # get keypress using getch, msvcrt = windows
    flag_have_getch = False
    flag_have_msvcrt = False
    try:
        import getch
        flag_have_getch = True
        first_char = getch.getch()
        if first_char == '\x1b':  # arrow keys
            a = getch.getch()
            b = getch.getch()
            return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[a + b]
        if ord(first_char) == 10:
            return 'enter'
        if ord(first_char) == 32:
            return 'space'
        else:
            return first_char  # normal keys like abcd 1234
    except:
        pass

    try:
        import msvcrt
        flag_have_msvcrt = True
        key = msvcrt.getch()  # get keypress
        if key == b'\x1b':  # Esc key to exit
            return 'esc'
        elif key == b'\r':  # Enter key to select
            return 'enter'
        elif key == b'\x48':  # Up or Down arrow
            return 'up'
        elif key == b'\x50':  # Up or Down arrow
            return 'down'
        else:
            return key.decode('utf-8')
    except:
        pass

    if flag_have_getch == False and flag_have_msvcrt == False:
        print('\nErr:\tcan\'t get input \nFix:\tpip install getch')
        exit()


def get_menu_choice(options, give_key_str=False):
    shortcuts = scan_short_cuts(options)  # scan for shortcuts
    selected_index = 0
    print(shortcuts)
    while True:
        show_menu(options, selected_index)
        key = get_key()
        if key == 'enter':  # Enter key to select
            return selected_index
        elif key in ('up', 'down', 's', 'w'):  # Up or Down arrow
            selected_index = (selected_index + (1 if key in ('down', 's') else -1) + len(options)) % len(options)
        elif key in shortcuts:  # Shortcut key
            show_menu(options, shortcuts[key])  # show selected option when using shortcut
            if (give_key_str):
                return key
            else:
                return shortcuts[key]


def scan_short_cuts(options):
    shortcuts = {}
    for i, option in enumerate(options):
        match = re.match(r"\[(.*)\](.*)", option)
        if match:
            shortcut, text = match.group(1, 2)
            shortcuts[shortcut] = i
    return shortcuts


def show_menu(options, selected_index):
    header()
    for i, option in enumerate(options):
        if i == selected_index:
            print(Fore.LIGHTCYAN_EX + "> " + Style.RESET_ALL + Fore.BLACK + Back.CYAN + option + Style.RESET_ALL)
        else:
            print(f"  {option}")
