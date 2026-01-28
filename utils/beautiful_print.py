import os
from colorama import Fore, Style


def beautiful_print(d, offset):
    for i in range(1, 11):
        try:
            item1, item2, item3 = (f'{i+30*offset}) {d[i+30*offset][1]}',
                                   f'{i+30*offset+10}) {d[i+30*offset+10][1]}',
                                   f'{i+30*offset+20}) {d[i+30*offset+20][1]}')
            print(item1 +" "*(40-len(item1)), end='')
            print(item2 +" "*(40-len(item2)), end='')
            print(item3)
        except KeyError:
            break
    print()

def header():
    os.system('cls')
    print(' ____      _    __     __ _____  ____\n'
          '/ ___|    / \   \ \   / /| ____||  _ \\\n'
          '\___ \   / _ \   \ \ / / |  _|  | |_) |\n'
          ' ___) | / ___ \   \ V /  | |___ |  _ <\n'
          '|____/ /_/   \_\   \_/   |_____||_| \_\\')
    print('    ' * 4 + Fore.RED + 'By Voynov 2025 1.3' + Style.RESET_ALL + '\n\n')