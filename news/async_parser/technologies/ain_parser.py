import asyncio

import aiohttp
from bs4 import BeautifulSoup
from django.db import IntegrityError

from news.models import *


async def ain_parser(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Технологии')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('div', class_='post-content').find('h1').text
            description = str(soup.find('div', class_='post-content'))
            picture = soup.find('div', class_='post-content').find('img').get('src')
            date = soup.find('meta', property='article:published_time').get('content')
            logo = 'https://i.ibb.co/10Q5qJH/ain.png'
            site = 'https://ain.ua/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='AIN', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_ain():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    url = 'https://ain.ua/post-list/'

    async with aiohttp.ClientSession() as session:
        tasks = []
        ain_response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await ain_response.text(), 'lxml')
        get_urls = soup.find('div', class_='posts-list')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(ain_parser(url.find('a').get('href'), session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass

        print(f"AiN - {len(tasks)} tasks")
        await asyncio.gather(*tasks)