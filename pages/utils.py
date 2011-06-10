def get_possible_exams():
	# There should only be two ... midterm and final
	# But in case we come across "practice" exams that are neither, we can add them
	return (
		('midterm', 'midterm'),
		('final', 'final'),
	)
