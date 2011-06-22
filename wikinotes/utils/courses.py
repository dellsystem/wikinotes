from django.core.exceptions import *
from wikinotes.models.faculties import Faculty
from wikinotes.models.courses import Course, CourseSemester
from wikinotes.models.pages import Page
from wikinotes.models.users import CourseWatcher
from wikinotes.utils.semesters import get_current_semester

def get_current_profs(course):
	try:
		professors = CourseSemester.objects.get(course=course, semester='Summer 2011').professors.all()
	except CourseSemester.DoesNotExist:
		# If the prof doesn't exist, return None, the template will take care of it
		return None
	return professors

def is_already_watching(user, course):
	try:
		CourseWatcher.objects.get(user=user, course=course)
		return True
	except CourseWatcher.DoesNotExist:
		return False
