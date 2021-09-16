import asyncio

from django.db import IntegrityError

from news.models import *

import aiohttp
from bs4 import BeautifulSoup


async def naked_science_parser(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Наука')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('div', class_='post-title').find('h1').text
            picture = soup.find('div', class_='post-image-inner').find('img').get('src')
            description = str(soup.find('div', class_='content').find('div', class_='body')).replace(str(soup.find('div', class_='content').find('div', class_='body').find('div', class_='shesht-social-sharing-block')), '').replace(str(soup.find('div', class_='content').find('div', class_='body').find('div', class_='typo_text')), '')
            date = soup.find('meta', property='article:published_time').get('content')
            logo = 'https://i.ibb.co/qysQd4s/naked-science.png'
            site = 'https://naked-science.ru/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Naked-science', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_naked_science():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    url = 'https://naked-science.ru/'

    async with aiohttp.ClientSession() as session:
        tasks = []
        naked_science_response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await naked_science_response.text(), 'lxml')
        get_urls = soup.find('div', class_='news-items')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(naked_science_parser(url.find('a').get('href'), session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass
        print(f"Naked-science - {len(tasks)} tasks")
        await asyncio.gather(*tasks)