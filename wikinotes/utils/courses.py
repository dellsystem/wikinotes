from django.core.exceptions import *
from wikinotes.models.faculties import Faculty
from wikinotes.models.courses import Course, CourseSemester
from wikinotes.models.pages import Page
from wikinotes.models.users import CourseWatcher
from wikinotes.utils.semesters import get_current_semester

def get_current_profs(course):
	try:
		professors = CourseSemester.objects.get(course=course, semester=get_current_semester()).professors
	except CourseSemester.DoesNotExist:
		# If the prof doesn't exist, return None, the template will take care of it
		return None
	return professors

# Get the number of watchers for this course
def get_num_watchers(course):
	num_watchers = CourseWatcher.objects.filter(course=course).count()
	return num_watchers

def get_num_pages(course):
	course_semester = CourseSemester.objects.filter(course=course)
	num_pages = Page.objects.filter(course_semester=course_semester).count()
	return num_pages

def is_already_watching(user, course):
	try:
		CourseWatcher.objects.get(user=user, course=course)
		return True
	except CourseWatcher.DoesNotExist:
		return False
