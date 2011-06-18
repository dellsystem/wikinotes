from django.http import HttpResponse
from wikinotes.models.faculties import Faculty
from wikinotes.models.departments import Department
from django.shortcuts import get_object_or_404

def overview(request, faculty_slug):
	# Gets passed the faculty slug
	faculty = get_object_or_404(Faculty, slug=faculty_slug)
	text = "You're looking at the page for the %s faculty" % faculty
	
	text += "<br />"
	
	# Now show a list of departments in this faculty
	departments = Department.objects.filter(faculty=faculty)
	for department in departments:
		text += "In this faculty we have this course: %s<br />" % department
	return HttpResponse(text)
