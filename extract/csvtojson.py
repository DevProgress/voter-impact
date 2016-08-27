#!/usr/bin/python

"""Convert congressional district vote data from CSV to a JSON form
that's easy to query in Javascript"""

import csv, json, sys, collections

for year in (2008, 2010, 2012, 2014):
    print('Converting %s' % year)
    ### Data structure we'll be dumping.
    ### Dictionary that maps "state-district" to an array of vote data
    ###   each vote is a dict of (first name, last name, party, votes, vote fraction, winner)
    vote_data = collections.defaultdict(list)

    ### Read the TSV in, build up the vote_data structure
    data_fn = "../data/%s-congress.tsv" % year
    with open(data_fn) as fp:
        reader = csv.DictReader(fp, dialect="excel-tab")
        for row in reader:
            key = "%s-%s" % (row['State'], row['District'])
            fields = ('First Name', 'Last Name', 'Party', 'Votes', 'Vote fraction', 'Winner')
            vote_data[key].append({ k: row[k] for k in fields })

    ### Write out the vote_data to JSON
    json_fn = "../data/%s-congress.json" % year
    with open(json_fn, 'w') as fp:
        json.dump(vote_data, fp, separators=(',', ':'))
