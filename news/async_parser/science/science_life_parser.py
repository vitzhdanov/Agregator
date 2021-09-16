import asyncio

from django.db import IntegrityError

from news.models import *

import aiohttp
from bs4 import BeautifulSoup


async def nkj_parser(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Наука')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('h1', itemprop='headline').text
            picture = soup.find('meta', property='og:image').get('content')
            date = soup.find('time', class_='nomer-god news-time').get('datetime')
            logo = 'https://i.ibb.co/WnznsPw/science-life.png'
            site = 'https://www.nkj.ru/'
            description = soup.find('article', class_='news-detail catalog-element').find('main')
            get_description = (str(description).replace(str(description.find('div', class_='figure-placeholder')), f'<div class="figure-placeholder"><img src="{picture}"></div>')).replace(str(description.find('div', class_='fullscreen-link')), '').replace(str(description.find('div', class_='swiper-button-next')), '').replace(str(description.find('div', class_='swiper-button-prev')), '')
            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Наука и жизнь', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=get_description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_nkj():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    url = 'https://nkj.ru/news/'

    async with aiohttp.ClientSession() as session:
        tasks = []
        nkj_response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await nkj_response.text(), 'lxml')
        get_urls = soup.find('section', class_='news-list')
        if get_urls is not None:
            for url in get_urls:
                try:
                    if len(url.find('a').get('href')) < 20:
                        task = asyncio.create_task(nkj_parser(f"https://nkj.ru{url.find('a').get('href')}", session))
                        tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass
        print(f"Наука и жизнь - {len(tasks)} tasks")
        await asyncio.gather(*tasks)