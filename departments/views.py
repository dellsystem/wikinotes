from django.http import HttpResponse

def department(request, department):
	text = "You are trying to view department information for the %s department" % department
	return HttpResponse(text)
