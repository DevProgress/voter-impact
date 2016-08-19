#!/usr/bin/env python3

"""Convert Sunlight Labs zip code -> district database to JSON
Source data: http://assets.sunlightfoundation.com/data/districts.csv
https://sunlightlabs.github.io/congress/index.html
"""

import csv, json, sys

### Data structure we're emitting.
### Dict of { zipcode: state-district }
data = {}
with open('../districts.csv') as fp:
    reader = csv.reader(fp)
    for row in reader:
        zipcode, state, district = row
        # Text format we're using in vote data. CA-03, for example
        v = "%s-%02d" % (state, int(district))
        data[zipcode] = v

json.dump(data, sys.stdout)