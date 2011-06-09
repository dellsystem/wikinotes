from django.shortcuts import render_to_response
from courses.models import Course

def course(request, department, number):
	this_course = Course.objects.get(department=department, number=int(number))
	description = this_course.get_description()
	return render_to_response('course/overview.html', locals())
