from django.http import HttpResponse

def user(request, username):
	text = "You are trying to view user information for the user of username %s" % username
	return HttpResponse(text)
