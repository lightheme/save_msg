import json
from utils.filters import filter_ascii
from tqdm.asyncio import tqdm as async_tqdm

global_chats = {}


async def update(client):
    count = 1
    is_premium = (await client.get_entity('me')).premium
    async for dialog in async_tqdm(client.iter_dialogs(), total=2000 if is_premium else 1000):
        global_chats[count] = [dialog.id, filter_ascii(dialog.name[:35])]
        count += 1

    with open('saver.config.json', "w") as f:
        json.dump(global_chats, f)