from django.http import HttpResponse
from wikinotes.models.departments import Department
from wikinotes.models.courses import Course
from django.shortcuts import get_object_or_404

def overview(request, department):
	# Gets passed the short name (4-char), which is the primary key
	department_name = get_object_or_404(Department, pk=department).get_long_name()
	text = "The %s department has a long name of %s" % (department, department_name)
	
	text += "<br />"
	
	# Now show a list of courses in this department
	courses = Course.objects.filter(department=department)
	for course in courses:
		text += "In this dept we have this course: %s<br />" % course
	return HttpResponse(text)
