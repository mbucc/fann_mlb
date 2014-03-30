#! /usr/bin/env python

from collections import namedtuple
import csv
import sys

import extract_data

to_year = from_year = int(sys.argv[1])

def header(columns_n):
	return '''
#include <stdio.h>
#include "floatfann.h"

int main()
{
    fann_type *calc_out;
    fann_type input[%d];

    struct fann *ann = fann_create_from_file("firstplace.net");

''' % (columns_n,)

def footer():
	return '''

    fann_destroy(ann);
    return 0;
}
'''


print >> sys.stderr, "Generating predictions for", to_year

#
# The training for year 2010 goes like this:
#    inputs are from 2008, 2009, 2010
#    output is from 2011 (1 = won division in 2011, 0 = did not win division)
#
# For this routine, if the input year is 2012, we assume you want the predictions for 2012.  
# So, to match how net was trained, we subtract one from each end of the year range.
training_rows, full_data_set, full_hash = extract_data.load_data(from_year - 1, to_year - 1)
columns_n = len(extract_data.columns_to_use) * (extract_data.years_to_look_back + 1)

print header(columns_n)
indent = "    "
for row in training_rows:
	input_columns = extract_data.inputs(row, full_data_set, full_hash)
	for i in range(len(input_columns)):
		print indent + "input[%d] = %s;" % (i, input_columns[i])
	print indent + "calc_out = fann_run(ann, input);"
	print indent + 'printf("%s-%s %s: %%7.4f %s\\n", calc_out[0]);' % (
			row.league, row.division, extract_data.division_winner_nextyear(row, full_hash), row.name)

print footer()
