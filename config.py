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