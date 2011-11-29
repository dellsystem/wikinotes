from django.shortcuts import render

def index(request):
	return render(request, 'contributing/index.html')

def moderating(request):
	return render(request, 'contributing/moderating.html')

def representatives(request):
	return render(request, 'contributing/representatives.html')

def development(request):
	return render(request, 'contributing/development.html')

def content(request):
	return render(request, 'contributing/content.html')

def guidelines(request):
	return render(request, 'contributing/guidelines.html')
