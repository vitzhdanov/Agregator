from bs4 import BeautifulSoup

import asyncio
import aiohttp
from django.db import IntegrityError

from news.models import *


async def mashable_parser(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Технологии')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    async with session.get(headers=headers, url=url) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('h1', class_='mt-4 header-100 max-w-5xl').text
            description = str(soup.find('article', class_='editor-content mt-8 font-serif'))
            picture = soup.find('div', class_='max-w-7xl px-4 mt-8 text-primary-400 font-sans mx-auto mt-10').find('img').get('src')
            date = soup.find('meta', property="article:published_time").get('content')
            logo = 'https://i.ibb.co/xCxJYC6/mashable.png'
            site = 'https://mashable.com/'
            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Mashable', site=site, category=category, title=title, picture=picture,
                            logo=logo, description=description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_mashable():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    url = 'https://mashable.com/tech'

    async with aiohttp.ClientSession() as session:
        tasks = []
        mashable_news = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await mashable_news.text(), 'lxml')
        get_urls = soup.find('div', class_='w-full justify-center mt-8')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(mashable_parser(f"https://mashable.com{url.find('a').get('href')}", session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass

        print(f"Mashable - {len(tasks)} tasks")
        await asyncio.gather(*tasks)