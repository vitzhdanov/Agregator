import asyncio

import json

import aiohttp

from bs4 import BeautifulSoup
from django.db import IntegrityError

from news.models import *


async def bleepingcomputer_parser(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Технологии')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('div', class_='article_section').find('h1').text
            description = str(soup.find('div', class_='articleBody'))
            picture = soup.find('div', class_='articleBody').find('img').get('src')
            date = json.loads(''.join(soup.find('script', type='application/ld+json').contents))['datePublished']
            logo = 'https://i.ibb.co/87nBVxY/bleepingcomputer.png'
            site = 'https://www.bleepingcomputer.com/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Bleepingcomputer', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError as ex:
            pass

        except IntegrityError:
            pass


async def gather_data_bleepingcomputer():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    url = 'https://www.bleepingcomputer.com/'

    async with aiohttp.ClientSession() as session:
        tasks = []
        bleepingcomputer_response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await bleepingcomputer_response.text(), 'lxml')
        get_urls = soup.find('ul', id='bc-home-news-main-wrap')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(bleepingcomputer_parser(url.find('a').get('href'), session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass
        print(f"Bleepingcomputer - {len(tasks)} tasks")
        await asyncio.gather(*tasks)