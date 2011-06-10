from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User as RealUser
from users.models import User

def user(request, username):
	this_user = get_object_or_404(RealUser, username=username)
	text = "You are trying to view user information for the user of username %s" % this_user
	return HttpResponse(text)
