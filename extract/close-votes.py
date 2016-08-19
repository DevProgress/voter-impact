"Figure out which votes were close, by district"

import json

data = json.load(open('../2012-congress.json'))
diffs = []
for district, votes in data.items():
    counts = [(int(v['Votes']), float(v['Vote fraction'])) for v in votes]
    counts.sort()
    if len(counts) >= 2:
        diffs.append((counts[-1][0] - counts[-2][0], counts[-1][1] - counts[-2][1], district))
diffs.sort()
print ("%7s\t%5s\t%6s" % ("Distr", "% Diff", "Votes Diff"))
for vote_diff, pct_diff, district in diffs:
    print ("%7s\t%5.2f\t%6d" % (district, 100*pct_diff, vote_diff))
