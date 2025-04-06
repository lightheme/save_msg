import asyncio
import json
import re
import sys

from tqdm.asyncio import tqdm as async_tqdm
import glob
import os
import sqlite3
from telethon import functions
from telethon.sync import TelegramClient
from tqdm import tqdm

api_id = 20188960
api_hash = "429cb9b90b420cf6ae70df4979c6a0fe"

client = TelegramClient('login',
                            api_id,
                            api_hash,
                            system_version='4.16.30-vxCUSTOM',
                            device_model='Tecno TECNO POVA 3',
                            lang_code='ru',
                            app_version='Telegram Android 10.6.5')
global_chats = {}


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
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

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
    print('    '*4+'By Voynov 2025'+'\n\n')

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
            with open(f'{dirname}/{msg.date.strftime("%d-%m-%Y_%H-%M-%S")}_{msg.id}.txt', 'w', encoding='UTF-8') as f:
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
    except (KeyboardInterrupt, RuntimeError):
        await client.disconnect()
        asyncio.get_event_loop().stop()
        client.loop.stop()

def set_chat(chat_name, chat_id):
    chats = get_chats()

    chats[chat_name] = chat_id
    with open('saver.config.json', "w") as f:
        json.dump(chats, f)


async def parse_new_chats(offset=0):
    header()
    beautiful_print(global_chats, offset)
    print('a) Предыдущие        0) Выход        d) Следующие\n\n')
    input_chats = await try_input('Выберите чат или чаты(написать через пробел): ')
    if input_chats.lower() == 'a':
        offset = 1 if offset==0 else offset
        return await parse_new_chats(offset - 1)
    elif input_chats.lower() == 'd':
        return await parse_new_chats(offset + 1)

    if not input_chats.replace(' ', "").isdigit():
        return
    if input_chats == '0':
        return
    choose_chats = [global_chats[int(inp)] for inp in input_chats.split(' ')]
    for chat in choose_chats:
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
            set_chat(chat, result.my_results[0].chat_id)

        return result.my_results[0]
    else:
        return await client.get_input_entity(chats[chat])


async def parse_saved_chats():
    workdirs = list(filter(lambda x: x.endswith('(saver)'), next(os.walk('.'))[1]))

    header()
    for i, dir in enumerate(workdirs):
        print(f'{i+1}) {dir.replace("(saver)", "")}')

    input_chats = await try_input('Выберите чат или чаты(написать через пробел): ')
    if input_chats == '0':
        return
    choose_chats = [[await find_chat(workdirs[int(inp) - 1]), workdirs[int(inp) - 1]] for inp in input_chats.split(' ')]
    for chat in choose_chats:
        await save_msgs(chat)


async def main():
    await client.start()
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
        print(f'1) Сохранить из новых чатов \n2) Сохранить из уже существующих чатов')
        choose = await try_input('Выберите вариант (1/2): ')

        if choose == '1':
            await parse_new_chats()
        elif choose == '2':
            await parse_saved_chats()

        os.system('cls')


if __name__ == '__main__':
    try:
        client.start()
        client.loop.create_task(main())
        client.run_until_disconnected()
    except sqlite3.OperationalError:
        for i in glob.glob(u'*.session'):
            os.unlink(i)
    except RuntimeError:
        asyncio.run(client.disconnect())
        asyncio.get_event_loop().stop()
        client.loop.stop()