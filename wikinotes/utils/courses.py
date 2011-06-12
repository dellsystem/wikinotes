from django.core.exceptions import *
from wikinotes.models.faculties import Faculty
from wikinotes.models.courses import Course, CourseSemester
from wikinotes.models.pages import Page
from wikinotes.models.users import CourseWatcher

# Gets a course object passed a tuple containing the term and the year (e.g. ('Winter', 2011))
def get_current_profs(course, semester):
	try:
		professors = CourseSemester.objects.get(course=course, term=term, year=year).professors
	except CourseSemester.DoesNotExist:
		# If the prof doesn't exist, return None, the template will take care of it
		return None
	return professors

# Get the number of watchers for this course
def get_num_watchers(course):
	num_watchers = CourseWatcher.objects.filter(course=course).count()
	return num_watchers

def get_num_pages(course):
	num_pages = Page.objects.filter(course=course).count()
	return num_pages

def is_already_watching(user, course):
	try:
		CourseWatcher.objects.get(user=user, course=course)
		return True
	except CourseWatcher.DoesNotExist:
		return False
