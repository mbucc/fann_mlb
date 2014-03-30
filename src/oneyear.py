#! /usr/bin/env python

from collections import namedtuple
import csv
import sys

years_to_look_back = 1
to_year = from_year = int(sys.argv[1])

Row = namedtuple('Row', [
      'year'                                # 1, Year     
    , 'league'                              # 2, League     
    , 'teamID'                              # 3, Team     
    , 'franchID'                            # 4, Franchise (links to TeamsFranchise table) 
    , 'division'                            # 5, Team's division    
    , 'rank'                                # 6, Position in final standings  
    , 'games_played'                        # 7, Games played    
    , 'games_played_at_home'                # 8, Games played at home  
    , 'wins'                                # 9, Wins     
    , 'losses'                              # 10, Losses     
    , 'division_winner'                     # 11, Division Winner (Y or N) 
    , 'wild_card_winner'                    # 12, Wild Card Winner (Y or N)
    , 'league_champion'                     # 13, League Champion(Y or N)  
    , 'world_series_winner'                 # 14, World Series Winner (Y or N)
    , 'runs'                                # 15, Runs scored    
    , 'at_bats'                             # 16, At bats    
    , 'hits'                                # 17, Hits by batters   
    , 'doubles'                             # 18, Doubles     
    , 'triples'                             # 19, Triples     
    , 'home_runs'                           # 20, Homeruns by batters   
    , 'walks'                               # 21, Walks by batters   
    , 'strikeouts_made'                     # 22, Strikeouts by batters   
    , 'stolen_bases'                        # 23, Stolen bases    
    , 'caught_stealing'                     # 24, Caught stealing    
    , 'hit_by_pitch'                        # 25, Batters hit by pitch  
    , 'sacrifice_flys'                      # 26, Sacrifice flies    
    , 'opponents_runs_scored'               # 27, Opponents runs scored   
    , 'earned_runs_allowed'                 # 28, Earned runs allowed   
    , 'earned_run_average'                  # 29, Earned run average   
    , 'complete_games'                      # 30, Complete games    
    , 'shutouts'                            # 31, Shutouts     
    , 'saves'                               # 32, Saves     
    , 'outs_pitched'                        # 33, Outs Pitched (innings pitched x 3)
    , 'hits_allowed'                        # 34, Hits allowed    
    , 'homeruns_allowed'                    # 35, Homeruns allowed    
    , 'walks_allowed'                       # 36, Walks allowed    
    , 'strikeouts_pitched'                  # 37, Strikeouts by pitchers   
    , 'errors'                              # 38, Errors     
    , 'double_plays'                        # 39, Double Plays    
    , 'fielding_percentage'                 # 40, Fielding percentage    
    , 'name'                                # 41, Team's full name   
    , 'park'                                # 42, Name of team's home ballpark 
    , 'attendance'                          # 43, Home attendance total   
    , 'batting_three_year_park_factor'      # 44, Three-year park factor for batters 
    , 'pitching_three_year_park_factor'     # 45, Three-year park factor for pitchers 
    , 'teamIDBR'                            # 46, Team ID used by Baseball Reference
    , 'teamIDlahman45'                      # 47, Team ID used in Lahman database
    , 'teamIDretro'                         # 48, Team ID used by Retrosheet 
    ])

#------------------------------------------------------------------------------
#
#                           M O D E L   I N P U T S 
#
#------------------------------------------------------------------------------

columns_to_use = (
      'games_played'                        # 7, Games played    
    , 'games_played_at_home'                # 8, Games played at home  
    , 'wins'                                # 9, Wins     
    , 'losses'                              # 10, Losses     
    , 'runs'                                # 15, Runs scored    
    , 'at_bats'                             # 16, At bats    
    , 'hits'                                # 17, Hits by batters   
    , 'doubles'                             # 18, Doubles     
    , 'triples'                             # 19, Triples     
    , 'home_runs'                           # 20, Homeruns by batters   
    , 'walks'                               # 21, Walks by batters   
    , 'strikeouts_made'                     # 22, Strikeouts by batters   
    , 'stolen_bases'                        # 23, Stolen bases    
    , 'caught_stealing'                     # 24, Caught stealing    
    , 'hit_by_pitch'                        # 25, Batters hit by pitch  
    , 'sacrifice_flys'                      # 26, Sacrifice flies    
    , 'opponents_runs_scored'               # 27, Opponents runs scored   
    , 'earned_runs_allowed'                 # 28, Earned runs allowed   
    , 'earned_run_average'                  # 29, Earned run average   
    , 'complete_games'                      # 30, Complete games    
    , 'shutouts'                            # 31, Shutouts     
    , 'saves'                               # 32, Saves     
    , 'outs_pitched'                        # 33, Outs Pitched (innings pitched x 3)
    , 'hits_allowed'                        # 34, Hits allowed    
    , 'homeruns_allowed'                    # 35, Homeruns allowed    
    , 'walks_allowed'                       # 36, Walks allowed    
    , 'strikeouts_pitched'                  # 37, Strikeouts by pitchers   
    , 'errors'                              # 38, Errors     
    , 'double_plays'                        # 39, Double Plays    
    , 'fielding_percentage'                 # 40, Fielding percentage    
    , 'attendance'                          # 43, Home attendance total   
    , 'batting_three_year_park_factor'      # 44, Three-year park factor for batters 
    , 'pitching_three_year_park_factor'     # 45, Three-year park factor for pitchers 
    )

#------------------------------------------------------------------------------
#
#                                  S C A L E 
#
#       We scale all the inputs within a division like this:
#
#
#                              (x - min) * 0.998
#                 scaled_x  = ------------------- + 0.001
#                                  max - min
#
#       Say, min = 40 and max = 80 
#        
#       OldRange = (OldMax - OldMin)  = 80 - 40 = 40 
#       NewRange = (NewMax - NewMin)  = 0.999 - 0.001 = 0.998
#       NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
#        
#       new40 = ((40 - 40) * 0.998)/40 + 0.001 = 0.001
#       new80 = ((80 - 40) * 0.998)/40 + 0.001 = 0.999
#------------------------------------------------------------------------------

def val(row, column):
	try:
		s = getattr(row, column)
		if s:
			return float(s)
		else:
			return 0.0
	except:
		raise Exception("Can't convert '%s' (%s) to float" % (getattr(row, column), column))

global league
global division
def scale(column, target_year, row, all_rows):
	global league
	global division
	oldmin = oldmax = val(row,column)
	league = row.league
	division = row.division
	for other in filter(by_division, all_rows):
		oldmin = min(oldmin, val(other, column))
		oldmax = max(oldmax, val(other, column))

	oldrange = oldmax - oldmin
	newmax = 0.999
	newmin = 0.001
	newrange = newmax - newmin

	return newmin + ((val(row, column) - oldmin) * newrange)/oldrange


#------------------------------------------------------------------------------
#
#                          I N P U T _ C O L U M N S 
#
#------------------------------------------------------------------------------

def input_columns(years_to_look_back, columns_to_use, row, all_rows):
	# >>> range(2010,2013)
	# [2010, 2011, 2012]
	yr = int(row.year)
	for target_year in range(yr - years_to_look_back + 1, yr + 1):
		i = 0
		for column in columns_to_use:
			s = "%5.4f" % (scale(column, target_year, row, all_rows),)
			if s == None:
				raise Exception("None for '%s' in %s" % (column, row))
			print "input[%d] = %s;" % (i, s)
			i += 1

 

#------------------------------------------------------------------------------
#
#                                F I L T E R S 
#
#------------------------------------------------------------------------------
def is_AL_east(row):
	global league
	global division
	division = 'E'
	league = 'AL'
	return by_division(row)

def by_year(row):
	return int(row.year) >= from_year and int(row.year) <= to_year

def by_division(row):
	return row.league == league and row.division == division

def header():
	return '''
#include <stdio.h>
#include "floatfann.h"

int main()
{
    fann_type *calc_out;
    fann_type input[33];

    struct fann *ann = fann_create_from_file("firstplace.net");

'''

def footer():
	return '''

    fann_destroy(ann);
    return 0;
}
'''

#------------------------------------------------------------------------------
#
#                   G E N E R A T E   M O D E L   I N P U T 
#
#------------------------------------------------------------------------------

#
# Train on all team statistics ...
#

#full_data_set  = map(Row._make, csv.reader(open("../dat/Teams.csv", "rb"))) 
full_data_set  = map(Row._make, csv.reader(sys.stdin))

#
# ... for relatively recent years.
#

training_rows = filter(by_year, full_data_set)

print header()

for row in training_rows:
	input_columns(years_to_look_back, columns_to_use, row, full_data_set)
	print "calc_out = fann_run(ann, input);"
	print 'printf("%s-%s %d: %%7.4f %s\\n", calc_out[0]);' % (row.league, row.division, int(row.rank), row.name)

print footer()
