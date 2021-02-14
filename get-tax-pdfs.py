import sys
import commons
import config
import requests
import os

results_per_page = config.results_per_page
config = config.config


if len(sys.argv) != 3:
    raise ValueError('You need to specify a form name and a range, example: "Form W-2" 2018-2020')

form_name = sys.argv[1]
year_range = sys.argv[2]

try:
    year_range = list(map(lambda x: int(x), year_range.split("-")))
    year_range.sort()
except:
    raise ValueError('Invalid year range, example valid year range: 2018-2020')

print("Starting extraction of PDFs for %s, over the %s range period" % (form_name, '%d-%d' % (year_range[0], year_range[-1])))

params = {**config['params'], 'value': form_name }
extracted_html = commons.get_page(0, params, 0)
if not extracted_html:
    raise Exception('Could not retrieve any results at the moment. Please try again later')

if not os.path.exists("pdf"):
    os.mkdir('pdf')

# Retrieve the total results number by parsing info from table
page_counters = commons.get_page_counters(extracted_html, results_per_page)
total_results = page_counters['total_results']
pages_cnt = page_counters['pages_cnt']

for page_num in range(pages_cnt):
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
        if int(fields[2]) < year_range[0] or int(fields[2])  > year_range[1]:
            continue

        download_url = row.find("a", href=True)["href"]
        r = requests.get(download_url)

        if r.status_code != requests.codes.ok:
            print("Could not retireve a PDF from %s, will skip this one and continue" % download_url)
            continue

        if not os.path.exists("pdf/%s" % fields[0]):
            os.mkdir("pdf/%s" % fields[0])
        f_name = 'pdf/%s/%s - %s.pdf' % (fields[0], fields[0], fields[2])
        with open(f_name, 'wb') as f:
            f.write(r.content)
            print('Successfully written PDF to %s' % f_name)

print('Done! Happy reading about taxes.')