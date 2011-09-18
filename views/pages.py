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
	}
	return render_to_response(page_type_obj.get_show_template(), data, context_instance=RequestContext(request))
