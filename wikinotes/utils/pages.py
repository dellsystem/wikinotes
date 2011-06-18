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
