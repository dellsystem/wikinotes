from django.http import HttpResponse

def course(request, department, id):
	text = "You are trying to view course information for %s %d" % (department, int(number))
	return HttpResponse(text)
