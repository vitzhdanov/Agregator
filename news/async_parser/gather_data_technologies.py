import time

from news.models import *

import asyncio

from news.async_parser.technologies.mashable_parser import gather_data_mashable
from news.async_parser.technologies.habr_parser import gather_data_habr
from news.async_parser.technologies.bleepingcomputer_parser import gather_data_bleepingcomputer
from news.async_parser.technologies.ain_parser import gather_data_ain
from news.async_parser.technologies.igate_parser import gather_data_igate
from news.async_parser.technologies.gagadget_parser import gather_data_gagadget


def main_technologies():
    if 'Технологии' not in str(Category.objects.all()):
        Category.objects.all().create(category='Технологии')
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_data_mashable())
    asyncio.run(gather_data_habr())
    asyncio.run(gather_data_bleepingcomputer())
    asyncio.run(gather_data_ain())
    asyncio.run((gather_data_igate()))
    asyncio.run(gather_data_gagadget())
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")