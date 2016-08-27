#!/usr/bin/env python3

"""Create a CSV showing Congress election results
Source data: http://www.fec.gov/pubrec/electionresults.shtml
This script emits general election results for House distracts and senate races"""

import xlrd
import csv, sys


for src_fn, dst_fn, src_sheets in (
    ('../data/results10.xls', '../data/2010-congress.tsv', ('2010 US House & Senate Results',)),
    ('../data/federalelections2012.xls', '../data/2012-congress.tsv', ('2012 US House & Senate Resuts',)),
    ('../data/results14.xls', '../data/2014-congress.tsv', ('2014 US Senate Results by State', '2014 US House Results by State')),

):
    print("Converting %s to %s" % (src_fn, dst_fn))
    with open(dst_fn, 'w') as fp:
        ### File IO
        wb = xlrd.open_workbook(src_fn)
        out = csv.writer(fp, dialect='excel-tab', quoting=csv.QUOTE_NONE, quotechar=None)

        # Output schema
        out.writerow(['State', 'District', 'First Name', 'Last Name', 'Party', 'Votes', 'Vote fraction', 'Winner'])

        for sheet_name in src_sheets:
            sheet = wb.sheet_by_name(sheet_name)
            rows = sheet.get_rows()

            ### CSV schema / headers
            # Source schema
            headers = [str(cell.value) for cell in next(rows)]
            col_index = {headers[i] : i for i in range(len(headers))}

            def v(r, name):
                "Extract the value for row r with column name n. Coerces to string."
                return str(r[col_index[name]].value).strip()

            ### Iterate through every row of data
            for row in rows:
                # See if a useful district is named in column D; this contains vote data
                if 'D' in col_index:
                    district = v(row, 'D')
                else:
                    district = v(row, 'DISTRICT')

                if district.endswith('.0'):
                    # Hack for districts marked as numbers, not strings
                    district = district[:-2]
                if len(district) > 0 and district != 'H':
                    # Looks like a useful record; emit the columns we care about
                    if 'GENERAL VOTES ' in col_index:
                        votes = row[col_index['GENERAL VOTES ']].value
                    else:
                        votes = row[col_index['GENERAL ']].value
                    try:
                        winner_indicator = v(row, 'GE WINNER INDICATOR')
                    except:
                        winner_indicator = ''
                    fractVote = row[col_index['GENERAL %']].value
                    if fractVote != "" and fractVote > 0:
                        out.writerow([
                            v(row, 'STATE ABBREVIATION'),
                            district,
                            v(row, 'CANDIDATE NAME (First)'),
                            v(row, 'CANDIDATE NAME (Last)'),
                            v(row, 'PARTY'),
                            "%d" % votes,
                            "%.5f" % fractVote,
                            winner_indicator])
