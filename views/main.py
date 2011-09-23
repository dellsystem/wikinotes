from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

def index(request):
	if request.user.is_authenticated():
		# Show the user's dashboard
		return render(request, 'main/dashboard.html')
	else:
		# Show the main page for logged-out users
		return render(request, 'main/index.html')

# POSTed to by the login form; should never be accessed by itself
def login_logout(request):
	# Check if the user is already logged in and is trying to log out
	if request.user.is_authenticated():
		if request.POST['logout']:
			logout(request)
	else:
		if request.POST['login']:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)

	# Redirect to the index page etc
	return index(request)
