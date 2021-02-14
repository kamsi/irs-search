import sys
import json
import re
import os
import commons
import config

results_per_page = config.results_per_page
config = config.config

if len(sys.argv) < 2:
    raise ValueError('At least one title is needed')

titles = sys.argv[1:]
print("Starting extraction of json results for %d titles" % len(titles))

if not os.path.exists("json"):
    os.mkdir('json')

for title in titles:
    print("Retrieving results for Title: %s" % title)
    title_results = []
    params = {**config['params'], 'value': title }
    extracted_html = commons.get_page(0, params, 0)
    if not extracted_html:
        print('Could not retrieve the first results page, skiping title %s' % title)
        continue
    # Retrieve the total results number by parsing info from table
    page_counters = commons.get_page_counters(extracted_html, results_per_page)
    total_results = page_counters['total_results']
    pages_cnt = page_counters['pages_cnt']
    min_year = None
    max_year = None

    for page_num in range(pages_cnt):
        sys.stdout.write('''\rProgress {0} / {1}'''.format(page_num + 1, pages_cnt))
        html = None
        # We already extracted the 0 page when getting total_results
        if page_num > 0:
            extracted_html = commons.get_page(page_num * results_per_page, params, page_num)
            if not extracted_html:
                continue

        rows = extracted_html.find_all("tr")
        # First 5 rows are irrelevant markup
        rows = rows[5:]
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
