print('[INFO] Приложение запускается...')
from tgClient.login import login
from tgClient.client import start_client, disconnecting
from chats import globally
from chats.globally import global_chats
from chats.parse import parse_new_chats, parse_saved_chats
from utils.beautiful_print import header
from colorama import init
import json
from menu import menu
import os

init()
client = login()
action_options = ['Сохранить из новых чатов ', 'Сохранить из уже существующих чатов', 'Обновить чаты', 'Выйти']


async def main():
    if not os.path.isfile('saver.config.json'):
        header()
        with open('saver.config.json', "w") as f:
            json.dump({}, f)
        await globally.update(client)

    while True:
        header()
        try:
            menu_entry_index = menu.get_menu_choice(action_options)+1
        except KeyboardInterrupt:
            await client.disconnecting()
            return
        if menu_entry_index == 1:
            await parse_new_chats(client)
        elif menu_entry_index == 2:
            await parse_saved_chats(client)
        elif menu_entry_index == 3:
            header()
            await globally.update(client)
        elif menu_entry_index == 4:
            await disconnecting(client)
            return

        os.system('cls')

if __name__ == '__main__':
    start_client(main(), client)