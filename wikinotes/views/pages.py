from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User as RealUser
from wikinotes.models.pages import Page
from wikinotes.models.courses import Course
from django.template import TemplateDoesNotExist
from wikinotes.forms.pages import *
from wikinotes.utils.pages import get_max_num_sections

def create(request, department, number, page_type):
	this_course = get_object_or_404(Course, department=department, number=int(number))
	
	# If the template specified by the page type exists, then we're good to go
	# Else, 404
	section_title = this_course
	# For initially creating the hidden sections on the page
	# For better degradation if javascript is disabled
	num_sections = xrange(1, get_max_num_sections()+1)
	try:
		# This is kind of inefficient maybe the types of pages should be db-governed later
		lecture_note_form = LectureNoteForm()
		past_exam_form = PastExamForm()
		return render_to_response('page/create-%s.html' % page_type, locals())
	except TemplateDoesNotExist:
		raise Http404
