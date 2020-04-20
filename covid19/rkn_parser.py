import os
import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import numpy as np
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.ERROR)
logger = logging.getLogger(__file__)

DATA_DIR = 'data'
BASE_URL = 'https://www.rospotrebnadzor.ru'
SEARCH_KEY_WORD = 'COVID-2019 в России'
START_DATE = '20.03.2020'
SEARCH_URL_TEMPLATE = '{}/search/index.php?tags=&q={}&where=iblock_news&how=d&from={}&to='
DATE_RE = re.compile(r'([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})')
ROW_DATA_RE = re.compile(r'([А-Я][А-яа-я \-\(\)]{3,})\s+(\d+)\s')


def parse_page(page_url):
    page = requests.get(page_url, verify=False)
    page_data = BeautifulSoup(page.content, 'lxml')
    return page_data


def get_feed_page(start_date, page_num=1):
    search_url = SEARCH_URL_TEMPLATE.format(BASE_URL, SEARCH_KEY_WORD, start_date)
    page_url = f'{search_url}&PAGEN_1={page_num}'
    page_data = parse_page(page_url)
    return page_data


def get_page_links(page_data):
    search_results = page_data.find('div', class_='search-page')
    page_links = search_results.find_all('a')

    def filter_page_link(page_link):
        if page_link.text == 'О подтвержденных случаях новой коронавирусной инфекции COVID-2019 в России':
            return True
        else:
            return False

    page_links = list(filter(lambda page_link: filter_page_link(page_link), page_links))
    return page_links


def fetch_data(start_date=START_DATE):
    print(f'Берем данные от {start_date}.')
    page_num = 1
    has_more_pages = True
    while has_more_pages:
        # Get feed page content.
        feed_page_data = get_feed_page(start_date, page_num=page_num)

        # Check if there is arrow link to the next page is present.
        has_more_pages = True if feed_page_data.find('a', class_='arrow') is not None else False

        # Get links to the single news pages related to COVID-19.
        feed_page_links = get_page_links(feed_page_data)

        for page_link in feed_page_links:
            page_url = '{}{}'.format(BASE_URL, page_link.attrs['href'])
            print('Process page:', page_url)

            page_data = parse_page(page_url)
            page_content = page_data.find('div', class_='news-detail')

            date = page_content.find('p', class_='date')
            dd, mm, yyyy = DATE_RE.search(date.text).groups()
            date_formatted = f'{yyyy}-{mm}-{dd}'

            try:
                filename = os.path.join(DATA_DIR, f'daily/{date_formatted}.csv')
                csv_file = open(filename, 'w')
                fieldnames = ['region', 'date', 'cases']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
            except Exception as err:
                logger.error(err)

            rows = ROW_DATA_RE.findall(page_content.text)
            for row in rows:
                region, count = row

                # Strip extra spaces and dashes.
                region = region.strip('-').strip(' ')

                # Region name could not have more than 5 words.
                if len(region.split(' ')) > 5:
                    continue

                try:
                    writer.writerow({'region': region, 'date': date_formatted, 'cases': count})
                except Exception as err:
                    logger.error(err)

            try:
                csv_file.close()
            except Exception as err:
                logger.error(err)

        # Try to go to the next page.
        page_num += 1


if __name__ == '__main__':
    fetch_data()
