import asyncio
import glob
import os
import sqlite3
from getpass import getpass

import qrcode
from telethon.errors import SessionPasswordNeededError


def print_qr_terminal(data: str) -> None:
    qr = qrcode.QRCode(border=1)
    qr.add_data(data)
    qr.make(fit=True)
    qr.print_ascii(invert=True)


def start_client(task, client):
    try:
        client.connect()
        if client.is_user_authorized():
            client.loop.create_task(task)
            client.run_until_disconnected()
            return

        choice = 0
        while choice not in (1, 2):
            os.system('cls')
            try:
                choice = int(input("Выберите способы аутентификации:\n1) По номеру телефона\n2) По QR-коду\nВаш выбор: "))
            except:
                pass
        if choice == 1:
            client.start(
                phone=lambda: input('Введите номер телефона в формате 7 XXX XXX XX XX: '),
                password=lambda: getpass('Введите облачный пароль: '),
                code_callback=lambda: input('Введите код который вам пришел: ')
            )
        elif choice == 2:

            qr = client.qr_login()
            print("\nОтсканируйте данный QR-код в телеграмм (Настройки -> Устройства -> Подключить устройство):\n")
            print_qr_terminal(qr.url)

            try:
                client.loop.run_until_complete(qr.wait())
            except SessionPasswordNeededError:
                pwd = input("\n2FA password: ").strip()
                client.sign_in(password=pwd)
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