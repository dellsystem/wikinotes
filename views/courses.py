from django.shortcuts import render_to_response, get_object_or_404
from wiki.models.courses import Course

def index(request):
	return render_to_response('courses/index.html')

def all(request):
	courses = Course.objects.all().order_by('department', 'number')
	data = {
		'courses': courses,
	}
	return render_to_response('courses/all.html', data)

def overview(request, department, number):
	course = get_object_or_404(Course, department=department, number=int(number))
	data = {
		'course': course,
	}
	return render_to_response('courses/overview.html', data)
