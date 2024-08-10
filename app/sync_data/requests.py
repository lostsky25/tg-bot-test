from os import path

import aiohttp

headers = {'User-Agent': 'Mozilla/5.0'}

async def get_all_categories(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = await response.json()
            return res

