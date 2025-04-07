import asyncio
import glob
import os
import sqlite3
from getpass import getpass


def start_client(task, client):
    try:
        client.start(
            phone=lambda: input('Введите номер телефона в формате 7 XXX XXX XX XX: '),
            password=lambda: getpass('Введите облачный пароль: '),
            code_callback=lambda: input('Введите код который вам пришел: ')
        )
        client.loop.create_task(task)
        client.run_until_disconnected()
    except sqlite3.OperationalError:
        for i in glob.glob(u'*.session'):
            os.unlink(i)
    except RuntimeError:
        asyncio.run(disconnecting(client))
        
async def disconnecting(client):
    await client.disconnect()
    asyncio.get_event_loop().stop()
    client.loop.stop()
    os.system('cls')