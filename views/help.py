from django.shortcuts import render

def index(request):
	return render(request, 'help/index.html')

def copyright(request):
	return render(request, 'help/copyright.html')

