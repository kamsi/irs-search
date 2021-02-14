<h1>IRS search</h1>

This are the 2 scripts which should complete 2 tasks asked for in the test.
It is assumed that python3 (my code was tested against Python 3.7.5) is installed together with pip.

<h2>Setup</h2>

1. Clone the repository
2. In the root folder run: pip install -r requirements.txt


<h2>Tasks</h2>

1. Taking a list of tax form names (ex: "Form W-2", "Form 1095-C"), search the
website and return some informational results. Specifically, you must return
the "Product Number", the "Title", and the maximum and minimum years the form
is available for download.

To use the script, run the setup instructions, then, from the root of the project execute:

python get-taxes-by-form-names.py 'Form W-2' 'Form 11-C'... <Your other form name>


The results are formatted as JSON and written under "json" directory. Example file path: json/Form W-2.json

2. Taking a tax form name (ex: "Form W-2") and a range of years (inclusive, 2018-
2020 should fetch three years), download all PDFs available within that range.
The downloaded PDFs should be downloaded to a subdirectory under your script's
main directory with the name of the form, and the file name should be the "Form
Name - Year" (ex: Form W-2/Form W-2 - 2020.pdf )

OK, so it should do the trick, yet it is not (yet?) optimized (probably some prallelism over final PDF requests would not harm).
To run the script, issue this from the root:

python get-tax-pdfs.py "Form W-2" 2019-2021

You can also pass single year as second param
The files are written according to given structure, except I also added pdf directory. So a result path to single PDF might look like `pdf/Form W-2`.
I did not want to clutter the root director.
