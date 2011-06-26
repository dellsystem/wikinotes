from django.shortcuts import render_to_response, get_object_or_404

def index(request):
	if request.user.is_authenticated():
		return render_to_response("dashboard.html", locals())
	else:
		return render_to_response("index.html", locals())
