from django.shortcuts import render_to_response, get_object_or_404
from wikinotes.models.courses import Course
from wikinotes.models.users import UserProfile

def index(request):
	this_user = request.user
	# For now, list all the classes we have on the index page
	courses = Course.objects.all()
	
	try:
		profile = UserProfile.objects.get(user=this_user)
	except:
		return render_to_response("index.html", locals())

	if this_user.is_authenticated():
		# Get the list of courses the user is watching
		watchers = profile.courses
		return render_to_response("dashboard.html", locals())
	else:
		return render_to_response("index.html", locals())
