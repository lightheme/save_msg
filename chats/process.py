import glob
import os
import re
from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm
from utils.beautiful_print import header


async def save_msgs(entity, client):
    header()
    off_id = 0
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

