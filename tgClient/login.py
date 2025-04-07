from telethon.sync import TelegramClient

def login():
    api_id = 21419117
    api_hash = "86f47ad119b57dc7797eb592468adde8"

    client = TelegramClient('login',
                            api_id,
                            api_hash,
                            system_version='4.16.30-vxCUSTOM',
                            device_model='SM-N975F',
                            lang_code='ru',
                            app_version='Telegram Android 10.6.5')

    return client