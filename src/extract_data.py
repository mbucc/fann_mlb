#! /usr/bin/env python
# Sat Mar 29 07:43:43 EDT 2014
# Get teams data we want, scale it, and get output (rank from year before).

from collections import namedtuple
import csv
import sys

# Model parameters
years_to_look_back = 2
from_year = 2000
to_year   = 2010

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
      'wins'                                # 9, Wins     
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

def scale(column, row, all_rows):

	oldmax = oldmin = val(row, column)

	for other in all_rows:
		if other.year     != row.year    : continue
		if other.league   != row.league  : continue
		if other.division != row.division: continue

		oldmin = min(oldmin, val(other, column))
		oldmax = max(oldmax, val(other, column))

	oldrange = oldmax - oldmin
	newmax = 0.999
	newmin = 0.001
	newrange = newmax - newmin

	# Some stats don't exist prior to 2000.
	if (oldrange == 0):
		return newmin
	

	return newmin + ((val(row, column) - oldmin) * newrange)/oldrange


#------------------------------------------------------------------------------
#
#                          I N P U T _ C O L U M N S 
#
#------------------------------------------------------------------------------

def inputs(row, all_rows, full_hash):
	# >>> range(2)
	# [0, 1]
	inputs = ()
	for offset in range(years_to_look_back + 1):
		key = row_to_key(row, -offset)
		row1 = full_hash[key]
		for column in columns_to_use:
			s = "%5.4f" % (scale(column, row1, all_rows),)
			if not s:
				raise Exception("None for '%s' in %s" % (column, row))
			inputs += (s,)
	return inputs

def outputs(row, full_hash):
	return division_winner_nextyear(row, full_hash)

 

#------------------------------------------------------------------------------
#
#                   G E N E R A T E   M O D E L   I N P U T 
#
#------------------------------------------------------------------------------

def row_to_key(row, yearoffset = 0):
	y = row.year

	# When teams changed name, the teamID also changes.
	tid = row.teamID
	tid_map = {
		  'MIA': 'FLO'
		, 'LAA': 'ANA'
		, 'MON': 'WAS'
	}
	tid = tid_map.get(tid, tid)

	if (yearoffset):
		y = str(int(y) + yearoffset)
	return (y, tid)

def rows_to_hash(rows):
	rval = {}
	for row in rows:
		rval[row_to_key(row)] = row
	return rval

def load_data(from_year, to_year):
	full_data_set  = map(Row._make, csv.reader(sys.stdin))
	training_rows = ()
	for row in full_data_set:
		if int(row.year) >= int(from_year) and int(row.year) <= int(to_year):
			training_rows += (row,)
	full_hash = rows_to_hash(full_data_set)
	return (training_rows, full_data_set, full_hash)

def division_winner(row):
	if row.division_winner == 'Y':
		return "1"
	elif row.division_winner == 'N':
		return "0"
	else:
		raise Exception("Unknown division_winner value '%s' in %s" % (row.division_winner, row))

def division_winner_nextyear(row, full_hash):
	key = row_to_key(row, 1)
	nextyear = full_hash[key]
	return division_winner(nextyear)

# Output the training model inputs (fann).  The The fann input format is:
#
#    line 1: <# training pairs> <# input columns> <# output columns>
#
#    The remaining lines come in pairs: 
#         - space-delimited input columns and 
#         - space-delimited output columns.

if __name__ == '__main__':
	training_rows, full_data_set, full_hash = load_data(from_year, to_year)

	print len(training_rows), len(columns_to_use) * (years_to_look_back + 1), 1
	for row in training_rows:
		print >> sys.stderr, "Processing %s %s %s: %s  ..." % (row.league, row.division, row.year, row.name)
		input_columns = inputs(row, full_data_set, full_hash)
		output_columns = outputs(row, full_hash)
		print " ".join(input_columns)
		print " ".join(output_columns)
