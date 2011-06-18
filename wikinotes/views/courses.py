from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from wikinotes.models.courses import Course, CourseSemester
from wikinotes.models.departments import Department
from wikinotes.utils.semesters import get_current_semester
from wikinotes.utils.courses import get_current_profs, get_num_watchers, get_num_pages, is_already_watching

def overview(request, department, number):

	# If it's a post request, do something

	this_course = get_object_or_404(Course, department=department, number=int(number))

	faculty = Department.objects.get(pk=department).faculty
	faculty_slug = faculty.slug
	
	description = this_course.get_description()
	course_name = this_course.get_name()
	credits = this_course.get_credits()
	
	# Get the current semester, and figure out the prof who is teaching this semester
	current_profs = get_current_profs(this_course)
	num_watchers = get_num_watchers(this_course)
	num_pages = get_num_pages(this_course)
	
	# Get all the semesters associated with this course (all the CourseSemesters)
	course_semesters = CourseSemester.objects.filter(course=this_course)
	
	# Show the "watch" button only for authenticated users
	this_user = request.user
	if this_user.is_authenticated():
		logged_in = True
		already_watching = is_already_watching(this_user, this_course)
	else:
		logged_in = False
		
	return render_to_response('course/overview.html', locals())

# Handles watch and unwatch requests by POST
def watch(request):
	if not request.POST:
		raise Http404
	
	user_id = request.POST.get('user')
	course_id = request.POST.get('course')
