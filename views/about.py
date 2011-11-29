from django.shortcuts import render

def index(request):
	return render(request, 'about/index.html', {'sections': ['About WikiNotes', 'The team', 'Legal information', 'Get involved', 'Press', 'Contact us']})

def history(request):
	return render(request, 'about/history.html')

def licensing(request):
	return render(request, 'about/licensing.html')

def platform(request):
	return render(request, 'about/platform.html')
