import datetime
import json

from bs4 import BeautifulSoup

import asyncio
import aiohttp
from django.db import IntegrityError

from news.models import *


async def gagadget_parser(session, url):
    news = News.objects.all()
    category = Category.objects.get(category='Технологии')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('div', class_='b-nodetop b-nodetop_nobor').text
            picture = f"https://gagadget.com{soup.find('div', class_='b-font-def post-links').find('img').get('src')}"
            description = soup.find('div', class_='b-font-def post-links')
            get_description = str(description).replace(description.find('img').get('src'), f"https://gagadget.com{description.find('img').get('src')}")
            get_date = soup.find('div', class_='bottom10 pull-left').text
            if get_date.split()[-2] == 'сегодня,':
                day = datetime.datetime.now().day
            else:
                day = datetime.datetime.now().day - 1
            time = get_date.split()[-1]
            month = datetime.datetime.now().strftime("%m")
            year = datetime.datetime.now().year
            date = f"{f'{year}-{month}-{day} {time}:00'.replace(' ', 'T')}-04:00"

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Gagadget', site=str('https://gagadget.com/'), category=category, title=title,
                            picture=picture, logo='https://i.ibb.co/tzcPfmr/gagadget.png', description=get_description, date=date)
        except AttributeError:
            pass

        except IntegrityError:
            pass

async def gather_data_gagadget():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    url_gagadget = 'https://gagadget.com/news/'

    async with aiohttp.ClientSession() as session:
        tasks = []

        gagadget_news = await session.get(url=url_gagadget, headers=headers)
        soup = BeautifulSoup(await gagadget_news.text(), 'lxml')
        get_urls = soup.find('div', class_='r-wide js-preload-content')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(gagadget_parser(session, f"https://gagadget.com{url.find('a').get('href')}"))
                    tasks.append(task)
                except:
                    continue
        else:
            pass
        print(f'GAGADGET - {len(tasks)}')
        await asyncio.gather(*tasks)