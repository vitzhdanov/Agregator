import asyncio

from django.db import IntegrityError

from news.models import *

import aiohttp
from bs4 import BeautifulSoup


async def hi_news_parser(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Наука')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('h1', class_='single-title').text
            description = str(soup.find('div', class_='text')).replace('data-src', 'src')
            picture = soup.find('div', class_='wp-caption alignnone').find('img').get('src')
            date = soup.find('time', class_='post__date').get('datetime')
            logo = 'https://i.ibb.co/rMJzRyb/hi-news.png'
            site = 'https://hi-news.ru/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Hi-News.ru', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_hi_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    url = 'https://hi-news.ru/'

    async with aiohttp.ClientSession() as session:
        tasks = []
        hi_news_response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await hi_news_response.text(), 'lxml')
        get_urls = soup.find('div', class_='roll main-roll')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(hi_news_parser(url.find('a').get('href'), session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass
        print(f"Hi-News - {len(tasks)} tasks")
        await asyncio.gather(*tasks)