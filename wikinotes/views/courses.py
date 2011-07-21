from wikinotes.models.courses import *
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from wikinotes.models.users import UserProfile
from wikinotes.models.pages import Page
from wikinotes.models.departments import Department
from wikinotes.utils.semesters import get_current_semester

def overview(request, department, number):

	# If it's a post request, do something

	this_course = get_object_or_404(Course, department=department, number=int(number))
	
	# Get the current semester, and figure out the prof who is teaching this semester
	current_profs = this_course.get_current_profs
	
	# Get all the semesters associated with this course (all the CourseSemesters)
	course_semesters = CourseSemester.objects.filter(course=this_course)
	
	# Get all the pages associated with any coursesemesters
	pages = Page.objects.filter(course_semester__course=this_course)
	for page in pages:
		page.term = page.course_semester.get_term().title()
		page.year = page.course_semester.get_year()
	
	# Show the "watch" button only for authenticated users
	this_user = request.user
	if this_user.is_authenticated():
		logged_in = True
		already_watching = this_course.is_user_watching(this_user)
	else:
		logged_in = False
		
	return render_to_response('course/overview.html', locals())

# Temporary view for handling watching
# Should be made into an AJAX request later, with a POST or something (how github does it)
def watch(request, department, number):
	this_user = request.user
	this_course = get_object_or_404(Course, department=department, number=int(number))
	
	# If the user is already watching the course, stop watching
	if this_course.is_user_watching(this_user):
		# Delete the database entry
		course_watcher = UserProfile.objects.get(user=this_user)
		course_watcher.courses.remove(this_course)
		success_title = 'Successfully unwatched course'
		success_message = 'No longer watching %s' % this_course
	else:
		# Create a database entry
		course_watcher = UserProfile(user=this_user)
		course_watcher.courses.add(this_course)
		success_title = 'Successfully watched course'
		success_message = 'You are now watching %s' % this_course
	
	return render_to_response('success.html', locals())
