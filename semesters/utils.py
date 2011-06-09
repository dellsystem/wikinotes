# For the possible years ...
import datetime

def get_possible_years():
	now = datetime.datetime.now()
	current_year = int(now.year)
	oldest_year = 2010
	years = xrange(oldest_year, current_year + 1)
	year_list = []
	for year in years:
		year_list.append((year, year))
	return year_list

def get_possible_terms():
	# Why not just hardcode it
	return (
		('Winter', 'Winter'),
		('Summer', 'Summer'),
		('Fall', 'Fall')
	)
