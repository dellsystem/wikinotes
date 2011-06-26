from django.shortcuts import render_to_response, get_object_or_404
from wikinotes.models.courses import Course

def index(request):
	# For now, list all the classes we have on the index page
	courses = Course.objects.all()
	if request.user.is_authenticated():
		return render_to_response("dashboard.html", locals())
	else:
		return render_to_response("index.html", locals())
