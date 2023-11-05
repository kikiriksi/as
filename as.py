import aiohttp
import requests
import asyncio
from bs4 import BeautifulSoup
import aiofiles
import os


async def dowload_wallpapers(session, url, name):
    async with aiofiles.open(f'pictures/{name.split("/")[1]}', mode='wb') as file:
        async with session.get(url) as response:
            async for chank in response.content.iter_chunked(2048):
                await file.write(chank)


async def main():
    url = 'https://asyncio.ru/zadachi/4/index.html'
    url_dowload = 'https://asyncio.ru/zadachi/4/'
    response = requests.get(url).text
    soup_image = [i['src'] for i in
                  BeautifulSoup(response, 'lxml').find('main').find_all('img')]
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(dowload_wallpapers(session, url_dowload + url, url)) for url in
                 soup_image]
        await asyncio.gather(*tasks)


asyncio.run(main())


def get_folder_size(filepath, size=0):
    for root, dirs, files in os.walk(filepath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size


print(get_folder_size('D:\python\pars_telegramm\pictures'))
