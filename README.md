<h1>IRS search</h1>

This are the 2 scripts which should complete 2 tasks asked for in the test.
It is assumed that python3 is installed together with pip.

<h2>Setup</h2>:

1. Clone the repository
2. In the root folder run: pip install -r requirements.txt


<h2>Tasks</h2>:

1. Taking a list of tax form names (ex: "Form W-2", "Form 1095-C"), search the
website and return some informational results. Specifically, you must return
the "Product Number", the "Title", and the maximum and minimum years the form
is available for download.

To use the script, run the setup instructions, then, from the root of the project execute:

python get-taxes-by-form-names.py 'Form W-2' 'Form 11-C'... <Your other form name>


The results are formatted as JSON and written under "json" directory. Example file path: json/Form W-2.json
