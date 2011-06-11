from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User as RealUser
from wikinotes.models.users import User

def profile(request, username):
	this_user = get_object_or_404(RealUser, username=username)
	text = "You are trying to view user information for the user of username %s, whose email is %s" % (this_user, this_user.email)
	return HttpResponse(text)
