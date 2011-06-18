from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User as RealUser
from wikinotes.models.pages import Page, PageType
from wikinotes.models.courses import Course
from wikinotes.models.departments import Department
from django.template import TemplateDoesNotExist
from wikinotes.forms.pages import PageForm
from wikinotes.utils.pages import get_max_num_sections

def create(request, department, number, page_type):
	this_course = get_object_or_404(Course, department=department, number=int(number))
	this_type = get_object_or_404(PageType, slug=page_type)
	if this_type.slug == 'exam':
		is_exam = True
	
	faculty = Department.objects.get(pk=department).faculty
	faculty_slug = faculty.slug
	
	# Does this type need a date
	need_date = this_type.need_date
	
	# If the template specified by the page type exists, then we're good to go
	# Else, 404
	section_title = this_course
	# For initially creating the hidden sections on the page
	# For better degradation if javascript is disabled
	num_sections = xrange(1, get_max_num_sections()+1)
	
	try:
		form = PageForm()
		return render_to_response('page/create.html', locals())
	except TemplateDoesNotExist:
		raise Http404
