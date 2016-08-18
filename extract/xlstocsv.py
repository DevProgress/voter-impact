#!/usr/bin/env python3

"""Create a CSV showing 2012 Congress election results
Source data: http://www.fec.gov/pubrec/fe2012/federalelections2012.shtml
This script emits general election results for House distracts and senate races"""

import xlrd
import csv, sys

src_fn = '../federalelections2012.xls'
src_sheet = '2012 US House & Senate Resuts'

# Open the sheet we care about
wb = xlrd.open_workbook(src_fn)
sheet = wb.sheet_by_name(src_sheet)
rows = sheet.get_rows()

# First row is spreadsheet schema, capture names of columns
headers = [str(cell.value) for cell in next(rows)]
col_index = {headers[i] : i for i in range(len(headers))}

def v(r, name):
    "Extract the value for row r with column name n. Coerces to string."
    return str(r[col_index[name]].value).strip()

# Iterate through every row of data

for row in rows:
    # See if a useful district is named in column D; this contains vote data
    district = v(row, 'D')
    if len(district) > 0 and district != 'H':
        # Extract votes and fractVote as numbers
        votes = row[col_index['GENERAL VOTES ']].value
        fractVote = row[col_index['GENERAL %']].value
        if fractVote != "" and fractVote > 0:
            print(
                v(row, 'STATE ABBREVIATION'),
                v(row, 'D'),
                v(row, 'CANDIDATE NAME (First)'),
                v(row, 'CANDIDATE NAME (Last)'),
                v(row, 'PARTY'),
                "%d" % votes,
                "%.5f" % fractVote,
                v(row, 'GE WINNER INDICATOR'))

# Write out a CSV file
