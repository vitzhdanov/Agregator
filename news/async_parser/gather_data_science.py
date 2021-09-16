import time

from news.models import *

import asyncio

from news.async_parser.science.naked_science_parser import gather_data_naked_science
from news.async_parser.science.science_life_parser import gather_data_nkj
from news.async_parser.science.hi_news_parser import gather_data_hi_news
from news.async_parser.science.sciencenews import gather_data_sciencenews


def main_science():
    if 'Наука' not in str(Category.objects.all()):
        Category.objects.all().create(category='Наука')
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_data_naked_science())
    asyncio.run(gather_data_nkj())
    asyncio.run(gather_data_hi_news())
    asyncio.run(gather_data_sciencenews())
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")