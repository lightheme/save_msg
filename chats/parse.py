import msvcrt
import os
import sys
from colorama import Back, Fore, Style
from telethon.tl import functions

from chats.globally import global_chats
from chats.process import save_msgs
from tgClient.client import disconnecting
from utils.beautiful_print import beautiful_print, header


async def try_input(text, client):
    try:
        return input(text)
    except (KeyboardInterrupt, RuntimeError, AttributeError):
        await disconnecting(client)


async def find_chat(chat, client):
    chat = chat.replace('(saver)', '')
    if chat not in global_chats:
        result = await client(functions.contacts.SearchRequest(
            q=chat,
            limit=10
        ))

        if result.my_results:
            result = result.my_results[0]
        elif result.results:
            result = result.results[0]

        return result
    else:
        return await client.get_input_entity(global_chats[chat])


async def parse_saved_chats(client):
    while True:
        workdirs = list(filter(lambda x: x.endswith('(saver)'), next(os.walk('.'))[1]))

        header()
        for i, dir in enumerate(workdirs):
            print(f'{i + 1}) {dir.replace("(saver)", "")}')
        print(
            Back.LIGHTGREEN_EX + Fore.BLACK + '\nEnter) Выбрать все' + '        ' + '0) НАЗАД ' + Style.RESET_ALL + '\n\n')

        input_chats = await try_input('Выберите чат или чаты(написать через пробел): ', client)
        if input_chats == '0':
            return
        if input_chats == '':
            choose_chats = [[await find_chat(workdir, client), workdir] for workdir in workdirs]
        elif not input_chats.replace(' ', "").isdigit():
            continue
        else:
            chats = list(filter(lambda x: int(x) < len(workdirs) or int(x) > 0, input_chats.strip().split()))
            choose_chats = [[await find_chat(workdirs[int(inp) - 1], client), workdirs[int(inp) - 1]] for inp in chats]
        for chat in choose_chats:
            await save_msgs(chat, client)


async def parse_new_chats(client):
    while True:
        def real_time_input(prompt='', input_str='', offset=0):
            header()
            beautiful_print(global_chats, offset)
            print(
                Back.LIGHTGREEN_EX + Fore.BLACK + 'a) Предыдущая        0) НАЗАД        d) Следующая ' + Style.RESET_ALL + '\n\n')
            sys.stdout.write(prompt)
            sys.stdout.write(input_str)
            sys.stdout.flush()

            while True:
                # py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
                char = msvcrt.getwch()
                if char == '\r':
                    sys.stdout.write('\n')
                    break
                elif char == '\x08':
                    if len(input_str) > 0:
                        input_str = input_str[:-1]
                        sys.stdout.write('\b \b')
                elif char.lower() in ('k', 'a', 'ф'):
                    os.system('cls')
                    offset = 1 if offset == 0 else offset
                    return real_time_input(prompt, input_str, offset - 1)
                elif char.lower() in ('m', 'd', 'в'):
                    os.system('cls')
                    return real_time_input(prompt, input_str, offset + 1)
                else:
                    if char != 'à':
                        sys.stdout.write(char)
                        input_str += char

                sys.stdout.flush()
            return input_str

        input_chats = real_time_input('Выберите чат или чаты(написать через пробел): ')

        if not input_chats.replace(' ', "").isdigit():
            continue
        if input_chats == '0':
            return
        chats = list(filter(lambda x: int(x) < len(global_chats) or int(x) > 0, input_chats.split()))
        choose_chats = [global_chats[int(inp)] for inp in chats]
        for chat in choose_chats:
            if chat[1] == 'NO KEY TABLE':
                continue
            # set_chat(chat[1], chat[0].id)
            await save_msgs(chat, client)