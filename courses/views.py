from django.shortcuts import render_to_response, get_object_or_404
from courses.models import Course
from semesters.models import CourseSemester
from semesters.utils import get_current_semester
from courses.utils import get_current_prof, get_num_watchers

def course(request, department, number):
	this_course = get_object_or_404(Course, department=department, number=int(number))
		
	description = this_course.get_description()
	course_name = this_course.get_name()
	credits = this_course.get_credits()
	
	# Get the current semester, and figure out the prof who is teaching this semester
	current_prof = get_current_prof(this_course, get_current_semester())
	num_watchers = get_num_watchers(this_course)
	
	# Get all the semesters associated with this course (all the CourseSemesters)
	course_semesters = CourseSemester.objects.filter(course=this_course)
	
	return render_to_response('course/overview.html', locals())
