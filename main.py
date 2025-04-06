from pystyle import Colorate, Colors

print('[INFO] Приложение запускается...')
from colorama import init, Fore, Back, Style
import asyncio
import json
import msvcrt
import re
from getpass import getpass
import sys
from telethon.tl.types import PeerChannel
import menu as dumb_menu
from tqdm.asyncio import tqdm as async_tqdm
import glob
import os
import sqlite3
from telethon import functions
from telethon.sync import TelegramClient
from tqdm import tqdm

api_id = 20188960
api_hash = "429cb9b90b420cf6ae70df4979c6a0fe"
init()
client = TelegramClient('login',
                            api_id,
                            api_hash,
                            system_version='4.16.30-vxCUSTOM',
                            device_model='Tecno TECNO POVA 3',
                            lang_code='ru',
                            app_version='Telegram Android 10.6.5')
global_chats = {}
supported_symbols = '''ёйцукенгшщзхъфывапролджэячсмитьбю'''+'''ёйцукенгшщзхъфывапролджэячсмитьбю'''.upper()
action_options = ['Сохранить из новых чатов ', 'Сохранить из уже существующих чатов', 'Выйти']

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

def filter_ascii(text):
    filtered_text = ''.join([i if ord(i) < 128 or i in supported_symbols else '' for i in text])
    return filtered_text if len(filtered_text.replace(' ', "")) > 0 else 'NO KEY TABLE'

async def aenumerate(aiterable):
    i = 0
    async for x in aiterable:
        yield i, x
        i += 1

async def aislice(aiterable, start=0, stop=sys.maxsize, step=1):
    it = iter(range(start, stop, step))
    try:
        nexti = next(it)
    except StopIteration:
        return
    async for i, element in aenumerate(aiterable):
        if i == nexti:
            yield element
            try:
                nexti = next(it)
            except StopIteration:
                return

def header():
    os.system('cls')
    print(' ____      _    __     __ _____  ____\n'
          '/ ___|    / \   \ \   / /| ____||  _ \\\n'
          '\___ \   / _ \   \ \ / / |  _|  | |_) |\n'
          ' ___) | / ___ \   \ V /  | |___ |  _ <\n'
          '|____/ /_/   \_\   \_/   |_____||_| \_\\')
    print('    ' * 4 + Fore.RED + 'By Voynov 2025 1.1.0' + Style.RESET_ALL + '\n\n')

async def save_msgs(entity, off_id=0):
    header()
    dirname = re.sub(r'[\\/:*?"<>|]', '_', entity[1]).replace("(saver)", '')+'(saver)'
    if not os.path.isdir(dirname):
        print('[INFO] Создание папки')
        os.mkdir(dirname)
    else:
        os.chdir(dirname)
        off_id = max([int(file.split('_')[-1:][0].replace('.txt', '')) for file in glob.glob("*.txt")])

        os.chdir("..")
    print(f'[INFO] Получаем сообщения из {entity[1]}')
    msgs = [msg async for msg in async_tqdm(client.iter_messages(entity[0], offset_id=off_id, reverse=True))]

    print(f"[INFO] Записываем сообщения из {entity[1]}")
    pbar = tqdm(total=len(msgs))
    for msg in msgs:
        if msg.text:
            with open(f'{dirname}/{msg.date.strftime("%Y-%m-%d_%H-%M-%S")}_{msg.id}.txt', 'w', encoding='UTF-8') as f:
                f.write(msg.text)
    pbar.close()
    print('[INFO] Все сообщения были записаны')

def get_chats():
    with open('saver.config.json') as f:
        chats = json.load(f)

    return chats

async def try_input(text=''):
    try:
        return input(text)
    except (KeyboardInterrupt, RuntimeError, AttributeError):
        await disconnectng()

def set_chat(chat_name, chat_id):
    chats = get_chats()

    chats[chat_name] = chat_id
    with open('saver.config.json', "w") as f:
        json.dump(chats, f)


async def parse_new_chats():
    while True:
        def real_time_input(prompt='', input_str='', offset=0):
            header()
            beautiful_print(global_chats, offset)
            print(Back.LIGHTGREEN_EX+Fore.BLACK+'a) Предыдущая        0) НАЗАД        d) Следующая \n\n'+Style.RESET_ALL)
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
            return
        if input_chats == '0':
            return
        choose_chats = [global_chats[int(inp)] for inp in input_chats.split(' ')]
        for chat in choose_chats:
            if chat[1] == 'NO KEY TABLE':
                continue
            set_chat(chat[1], chat[0].id)
            await save_msgs(chat)


async def find_chat(chat):
    chats = get_chats()
    chat = chat.replace('(saver)', '')
    if chat not in chats:
        result = await client(functions.contacts.SearchRequest(
            q=chat,
            limit=10
        ))

        if result.my_results[0]:
            if isinstance(result.my_results[0], PeerChannel):
                set_chat(chat, result.my_results[0].channel_id)
            else:
                set_chat(chat, result.my_results[0].chat_id)

        return result.my_results[0]
    else:
        return await client.get_input_entity(chats[chat])


async def parse_saved_chats():
    while True:
        workdirs = list(filter(lambda x: x.endswith('(saver)'), next(os.walk('.'))[1]))

        header()
        for i, dir in enumerate(workdirs):
            print(f'{i+1}) {dir.replace("(saver)", "")}')
        print(Back.LIGHTGREEN_EX+Fore.BLACK+'\nEnter) Выбрать все'+'        '+'0) НАЗАД \n\n'+Style.RESET_ALL)

        input_chats = await try_input('Выберите чат или чаты(написать через пробел): ')
        if input_chats == '0':
            return
        if input_chats == '':
            choose_chats = [[await find_chat(workdir), workdir] for workdir in workdirs]
        else:
            choose_chats = [[await find_chat(workdirs[int(inp) - 1]), workdirs[int(inp) - 1]] for inp in input_chats.strip(' ').split(' ')]
        for chat in choose_chats:
            await save_msgs(chat)


async def main():
    if not os.path.isfile('saver.config.json'):
        with open('saver.config.json', "w") as f:
            json.dump({}, f)

    is_premium = (await client.get_entity('me')).premium
    header()
    if len(global_chats)==0:
        count = 1
        async for dialog in async_tqdm(client.iter_dialogs(), total=2000 if is_premium else 1000):
            global_chats[count] = [dialog, filter_ascii(dialog.name[:35])]
            count+=1

    while True:
        header()
        try:
            menu_entry_index = dumb_menu.get_menu_choice(action_options, isclean = True)+1
        except KeyboardInterrupt:
            await disconnectng()
            return
        if menu_entry_index == 1:
            await parse_new_chats()
        elif menu_entry_index == 2:
            await parse_saved_chats()
        elif menu_entry_index == 3:
            await disconnectng()
            return

        os.system('cls')

async def disconnectng():
    await client.disconnect()
    asyncio.get_event_loop().stop()
    client.loop.stop()
    os.system('cls')


if __name__ == '__main__':
    try:
        client.start(
            phone=lambda: input('Введите номер телефона в формате 7 XXX XXX XX XX: '),
            password=lambda: getpass('Введите облачный пароль: '),
            code_callback=lambda: input('Введите код который вам пришел: ')
        )
        client.loop.create_task(main())
        client.run_until_disconnected()
    except sqlite3.OperationalError:
        for i in glob.glob(u'*.session'):
            os.unlink(i)
    except RuntimeError:
        asyncio.run(disconnectng())