from semesters.models import Semester, CourseSemester
from django.core.exceptions import *
from users.models import CourseWatcher
from pages.models import Page

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
