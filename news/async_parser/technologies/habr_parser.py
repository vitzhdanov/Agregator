from bs4 import BeautifulSoup

import asyncio
import aiohttp
from django.db import IntegrityError

from news.models import *


async def habr_parser(session, url):
    news = News.objects.all()
    category = Category.objects.get(category='Технологии')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('div', class_='tm-page-article__head-wrapper').find('h1').text
            description = str(soup.find('div', class_='article-formatted-body article-formatted-body_version-2')).replace('data-src', 'src')
            picture = soup.find('figure', class_='full-width').find('img').get('data-src')
            date = soup.find('span', class_='tm-article-snippet__datetime-published').find('time').get('datetime')
            logo = 'https://i.ibb.co/sqVQ6DZ/image.png'
            site = 'https://habr.com/ru/news/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Хабр', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_habr():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    url_habr = 'https://habr.com/ru/news/'

    async with aiohttp.ClientSession() as session:
        tasks = []
        habr_news = await session.get(url=url_habr, headers=headers)
        soup = BeautifulSoup(await habr_news.text(), 'lxml')
        get_urls = soup.find('div', class_='tm-articles-list')
        for url in get_urls:
            try:
                task = asyncio.create_task(habr_parser(session, f"https://habr.com{url.find('a', class_='tm-article-snippet__title-link').get('href')}"))
                tasks.append(task)
            except:
                continue

        print(f"Хабр - {len(tasks)} tasks")
        await asyncio.gather(*tasks)