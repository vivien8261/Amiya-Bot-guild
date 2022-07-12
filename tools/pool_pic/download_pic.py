import os
import json
import asyncio

from fake_useragent import UserAgent
from amiyabot.network.download import download_async

ua = UserAgent()

if not os.path.exists('resource/pool'):
    os.makedirs('resource/pool')


async def start():
    with open('pool.json', mode='r', encoding='utf-8') as f:
        pools = json.load(f)

    for item in pools:
        name = item['filename']
        url = item['url']

        if os.path.exists(f'resource/pool/{name}'):
            continue

        print(f'download {name}')

        res = await download_async(url, headers={'User-Agent': ua.random})
        if res:
            with open(f'resource/pool/{name}', mode='wb') as f:
                f.write(res)


asyncio.run(start())
