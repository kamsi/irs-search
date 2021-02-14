import requests
from bs4 import BeautifulSoup
import config
import re
import math

def get_page(from_index, params, page_num):
    params['indexOfFirstRow'] = from_index
    r = requests.get(config.config['baseUrl'], params=params)
    if r.status_code != requests.codes.ok:
        print('Ups, something went wrong, could not retrieve page %d, will continue without it' % page_num)
        return
    return BeautifulSoup(r.text, 'html.parser')

def get_page_counters(extracted_html, results_per_page):
    search_fields_table = extracted_html.find('table', class_='searchFieldsTable')
    pagination = search_fields_table.find('th', class_='ShowByColumn')
    pagination = pagination.get_text().strip().replace('\n', '')
    total_results = int(re.sub(r'.+ of (\d+?) files.*', r'\1', pagination))
    pages_cnt = math.ceil(total_results / results_per_page)

    return {
        'total_results': total_results,
        'pages_cnt': pages_cnt
    }
