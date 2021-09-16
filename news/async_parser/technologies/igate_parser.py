import asyncio

import aiohttp
from bs4 import BeautifulSoup

import json

from django.db import IntegrityError

from news.models import *


async def igate_parser(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Технологии')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('title').text
            description = str(soup.find('div', class_='entry-content post'))
            picture = f"https://igate.com.ua{soup.find('div', class_='entry-content post').find('img').get('src')}"
            date = f"{json.loads(''.join(soup.find('script', type='application/ld+json').contents))['datePublished'].replace(' ', 'T')}-04:00"
            logo = 'https://i.ibb.co/K6wjhTx/IG.png'
            site = 'https://igate.com.ua/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='iGate', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_igate():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    url = 'https://igate.com.ua/category/tehnologii'

    async with aiohttp.ClientSession() as session:
        tasks = []
        igate_response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await igate_response.text(), 'lxml')
        get_urls = soup.find('div', class_='masonry-wrapper')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(igate_parser(f"https://igate.com.ua{url.find('a').get('href')}", session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass
        print(f"iGate - {len(tasks)} tasks")
        await asyncio.gather(*tasks)