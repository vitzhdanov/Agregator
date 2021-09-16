import asyncio

from django.db import IntegrityError

from news.models import *

import aiohttp
from bs4 import BeautifulSoup


async def sciencenews_parser_paleontology(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Наука')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('h1', class_='header-default__title___2wL7r').text
            description = str(soup.find('div', class_='rich-text single__rich-text___BlzVF')).replace(str(soup.find('div', class_='rich-text single__rich-text___BlzVF').find('section')), '')
            picture = soup.find('div', class_='header-default__thumbnail___3TQ8l').find('img').get('src')
            date = soup.find('time', class_='date entry-date byline__published___3GjAo').get('datetime')
            logo = 'https://i.ibb.co/9bJxb3J/sciencenews.png'
            site = 'https://www.sciencenews.org/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Science News', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass


async def sciencenews_parser_neuroscience(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Наука')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('h1', class_='header-default__title___2wL7r').text
            description = str(soup.find('div', class_='rich-text single__rich-text___BlzVF')).replace(str(soup.find('div', class_='rich-text single__rich-text___BlzVF').find('section')), '')
            picture = soup.find('div', class_='header-default__thumbnail___3TQ8l').find('img').get('src')
            date = soup.find('time', class_='date entry-date byline__published___3GjAo').get('datetime')
            logo = 'https://i.ibb.co/9bJxb3J/sciencenews.png'
            site = 'https://www.sciencenews.org/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Science News', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass

async def sciencenews_parser_genetics(url, session):
    news = News.objects.all()
    category = Category.objects.get(category='Наука')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            title = soup.find('h1', class_='header-default__title___2wL7r').text
            description = str(soup.find('div', class_='rich-text single__rich-text___BlzVF')).replace(str(soup.find('div', class_='rich-text single__rich-text___BlzVF').find('section')), '')
            picture = soup.find('div', class_='header-default__thumbnail___3TQ8l').find('img').get('src')
            date = soup.find('time', class_='date entry-date byline__published___3GjAo').get('datetime')
            logo = 'https://i.ibb.co/9bJxb3J/sciencenews.png'
            site = 'https://www.sciencenews.org/'

            try:
                if title in news.get(title=title).title:
                    pass
            except:
                news.create(name='Science News', site=site, category=category, title=title, picture=picture,
                                logo=logo, description=description, date=date)

        except AttributeError:
            pass

        except IntegrityError:
            pass


async def gather_data_sciencenews():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    url = 'https://www.sciencenews.org/topic/paleontology'
    url_2 = 'https://www.sciencenews.org/topic/neuroscience'
    url_3 = 'https://www.sciencenews.org/topic/genetics'

    async with aiohttp.ClientSession() as session:
        tasks = []

        sciencenews_response_p = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await sciencenews_response_p.text(), 'lxml')
        get_urls = soup.find('ol', class_='river-with-sidebar__list___1EfmS')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(sciencenews_parser_paleontology(url.find('a').get('href'), session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass

        sciencenews_response_n = await session.get(url=url_2, headers=headers)
        soup = BeautifulSoup(await sciencenews_response_n.text(), 'lxml')
        get_urls = soup.find('ol', class_='river-with-sidebar__list___1EfmS')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(sciencenews_parser_neuroscience(url.find('a').get('href'), session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass

        sciencenews_response_g = await session.get(url=url_3, headers=headers)
        soup = BeautifulSoup(await sciencenews_response_g.text(), 'lxml')
        get_urls = soup.find('ol', class_='river-with-sidebar__list___1EfmS')
        if get_urls is not None:
            for url in get_urls:
                try:
                    task = asyncio.create_task(sciencenews_parser_genetics(url.find('a').get('href'), session))
                    tasks.append(task)
                except AttributeError:
                    continue
        else:
            pass
        print(f"Science News Paleontology - {len(tasks)} tasks")
        await asyncio.gather(*tasks)

