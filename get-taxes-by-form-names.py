import sys
import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import re
import math

results_per_page = 200

config = {
    'baseUrl': 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html',
    'params': {
        'resultsPerPage': results_per_page,
        'sortColumn': 'currentYearRevDate',
        'indexOfFirstRow': 0,
        'criteria': 'formNumber',
        'isDescending': 'false'
    }
}

if len(sys.argv) < 2:
    raise ValueError('At least one title is needed')

titles = sys.argv[1:]

print("Starting extraction of json results for %d titles" % len(titles))
for title in titles:
    print("Retrieving results for Title: %s" % title)
    title_results = []
    params = {**config['params'], 'value': title }
    r = requests.get(config['baseUrl'], params=params)
    extracted_html = BeautifulSoup(r.text, 'html.parser')
    if r.status_code != requests.codes.ok:
        print('Could not retrieve the first results page, skiping title %s' % title)
    # Retrieve the total results number by parsing info from table
    search_fields_table = extracted_html.find('table', class_='searchFieldsTable')
    pagination = search_fields_table.find('th', class_='ShowByColumn')
    pagination = pagination.get_text().strip().replace('\n', '')
    total_results = int(re.sub(r'.+ of (\d+?) files.*', r'\1', pagination))
    pages_cnt = math.ceil(total_results / results_per_page)

    for page_num in range(pages_cnt):
        sys.stdout.write('''\rProgress {0} / {1}'''.format(page_num + 1, pages_cnt))
        html = None
        # We already extracted the 0 page when getting total_results
        if page_num > 0:
            params['indexOfFirstRow'] = page_num * results_per_page
            r = requests.get(config['baseUrl'], params=params)
            if r.status_code != requests.codes.ok:
                print('Ups, something went wrong, could not retrieve page %d, will continue without it' % page_num)
                continue
            extracted_html = BeautifulSoup(r.text, 'html.parser')

        rows = extracted_html.find_all("tr")
        # First 5 rows are irrelevant markup
        rows = rows[5:]
        min_year = None
        max_year = None
        for row in rows:
            fields = list(map(lambda x: x.get_text().strip(), row.find_all("td")))
            if not min_year or min_year > fields[2]:
                min_year = fields[2]
            if not max_year or max_year < fields[2]:
                max_year = fields[2]

            title_results.append({
                "form_number": fields[0],
                "form_title": fields[1],
            })

    # This can be done better:
    # there is sorting on the year column, so that could have been achieved by 1 extra request and reading value from first and last item
    # only I noticed after having written this and... I believe this works good enough
    for item in title_results:
        item['min_year'] = min_year
        item['max_year'] = max_year

    sys.stdout.write('''\rProgress {0} / {1}'''.format(page_num + 1, pages_cnt))

    with open('json/%s.json' % title, 'w') as f:
        f.write(json.dumps(title_results, indent=2))
        sys.stdout.write('''\nAll done for %s, results written to json/%s.json\n''' % (title, title))
