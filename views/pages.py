from django.shortcuts import render_to_response, get_object_or_404
from wiki.models.courses import Course, CourseSemester
from utils import page_types as types
from django.template import RequestContext
from wiki.models.pages import Page

def show(request, department, number, page_type, term, year, slug):
	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	page_type_obj = types[page_type]
	data = {
		'course': course,
		'page': page,
		'sections': page.load_sections(page_type_obj),
		'show_template': page_type_obj.get_show_template(),
		'edit_url': page.get_url() + '/edit',
	}
	return render_to_response("pages/show.html", data, context_instance=RequestContext(request))

def edit(request, department, number, page_type, term, year, slug):
	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	page_type_obj = types[page_type]
	
	data = {
		'course': course,
		'page': page, # to distinguish it from whatever
		'field_templates': page_type_obj.get_field_templates(),
		'num_sections': range(1, 11),
		'help_template': page_type_obj.get_help_template(),
		'sections': page.load_sections(page_type_obj),
		'num_sections': range(1, 11) if page.num_sections < 11 else range(1, page.num_sections + 1), # check on this later
		'terms': ['winter', 'summer', 'fall'], # fix this later
		'years': range(2011, 1999, -1),
	}
	return render_to_response("pages/edit.html", data, context_instance=RequestContext(request))
	
