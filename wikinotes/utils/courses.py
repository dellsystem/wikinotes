from django.core.exceptions import *
# from wikinotes.models import CourseWatcher, Semester, CourseSemester, Page
from wikinotes.models.faculties import Faculty
from wikinotes.models.courses import *
from wikinotes.models.semesters import *
from wikinotes.models.pages import *
from wikinotes.models.users import CourseWatcher
import datetime

# Gets a course object passed a tuple containing the term and the year (e.g. ('Winter', 2011))
def get_current_prof(course, semester):
	semester = Semester.objects.get(term=semester[0], year=semester[1])
	try:
		prof = CourseSemester.objects.get(course=course, semester=semester).get_prof()
	except ObjectDoesNotExist:
		# If the prof doesn't exist, return None, the template will take care of it
		return None
	return prof

# Get the number of watchers for this course
def get_num_watchers(course):
	num_watchers = CourseWatcher.objects.filter(course=course).count()
	return num_watchers

def get_num_pages(course):
	num_pages = Page.objects.filter(course=course).count()
	return num_pages

# For the possible years ...
import datetime

def get_possible_years():
	now = datetime.datetime.now()
	current_year = int(now.year)
	oldest_year = 1995
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
