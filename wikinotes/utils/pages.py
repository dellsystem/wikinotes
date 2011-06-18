import calendar

def get_possible_exams():
	# There should only be two ... midterm and final
	# But in case we come across "practice" exams that are neither, we can add them
	return (
		('midterm', 'Midterm'),
		('final', 'Final'),
	)

# For choices
def get_possible_numbers(minimum, maximum):
	numbers = xrange(minimum, maximum+1)
	numbers_list = []
	for number in numbers:
		numbers_list.append((number, number))
	return numbers_list

# Defined here for easy changing, like a pseudo-constant
def get_max_num_sections():
	return 10

# Monday - Friday, and the months, and the days
def get_weekday_dates():
	pass

def get_possible_weekdays():
	# meh
	weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] # and saturday comes after apparently
	to_return = []
	for weekday in weekdays:
		to_return.append((weekday.lower(), weekday))
	return to_return

# Show all the possible months, then later use Javascript to delete the unnecessary ones for this semester
def get_possible_months():
	month_list = []
	for month in calendar.month_name:
		if month != '':
			month_list.append((month.lower(), month))
	return month_list
