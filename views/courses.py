from django.shortcuts import render_to_response
from wiki.models.courses import Course

def index(request):
	return render_to_response('courses/index.html')

def all(request):
	pass
