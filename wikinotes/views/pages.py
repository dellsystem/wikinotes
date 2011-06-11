from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User as RealUser
from wikinotes.models.pages import Page

def create(request, department, number, page_type):
	text = "lol"
	return HttpResponse(text)
