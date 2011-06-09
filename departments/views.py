from django.http import HttpResponse
from departments.models import Department
from courses.models import Course

def department(request, department):
	# Gets passed the short name (4-char), which is the primary key
	department_name = Department.objects.get(pk=department).get_long_name()
	text = "The %s department has a long name of %s" % (department, department_name)
	
	text += "<br />"
	
	# Now show a list of courses in this department
	courses = Course.objects.filter(department=department)
	for course in courses:
		text += "In this dept we have this course: %s<br />" % course
	return HttpResponse(text)
