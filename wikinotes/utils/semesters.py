# For the possible years ...
import datetime

def get_possible_years(start):
	now = datetime.datetime.now()
	current_year = int(now.year)
	years = xrange(start, current_year + 1)
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
	
def get_current_semester():
	now = datetime.datetime.now()
	# Okay for now just hardcoding dates:
	# January 1 to April 30, winter
	# May 1 to August 31, summer
	# September 1 to December 31, fall
	
	month = now.month
	if month >= 1 and month < 5:
		term = "Winter"
	elif month >= 5 and month < 9:
		term = "Summer"
	else:
		term = "Fall"
	
	year = now.year
	
	# Return a tuple - the term and the year
	return (term, year)
