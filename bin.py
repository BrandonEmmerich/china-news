#! /Users/b/anaconda2/bin/python
import pandas as pd
import web

# Sweep Process ----------------------------------------------------------------
sweep_results = web.get_urls()

# Scrape Process ---------------------------------------------------------------
results_list = []
errors = []
errors_final = []

for url in sweep_results:
    try:
        data = web.get_yicai(url)

        if data:
            results_list.append(data)

    except Exception as e:
        print "We had an error, adding to the errors queue!  Exception: {}".format(e)
        errors.append(url)

# Retries
for url in errors:
    try:
        data = web.get_yicai(url)

        if data:
            results_list.append(data)

    except Exception as e:
        print "We had an error, adding to the errors queue!  Exception: {}".format(e)
        errors_final.append(url)


flat_list = [item for sublist in results_list for item in sublist]
# Process Data -----------------------------------------------------------------

web.write_data_to_db(results_list)

print len(results_list)
print len(errors)
print len(errors_final)
