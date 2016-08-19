#!/usr/bin/python

"""Convert 2012 congressional district vote data to a JSON form
that's easy to query in Javascript"""

import csv, json, sys, collections

### Data structure we'll be dumping.
### Dictionary that maps "state-district" to an array of vote data
###   each vote is a dict of (first name, last name, party, votes, vote fraction, winner)
vote_data = collections.defaultdict(list)

### Read the TSV in, build up the vote_data structure
data_fn = "../out.tsv"
with open(data_fn) as fp:
    reader = csv.DictReader(fp, dialect="excel-tab")
    for row in reader:
        key = "%s-%s" % (row['State'], row['District'])
        fields = ('First Name', 'Last Name', 'Party', 'Votes', 'Vote fraction', 'Winner')
        vote_data[key].append({ k: row[k] for k in fields })

### Write out the vote_data to JSON
json.dump(vote_data, sys.stdout)
