from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User as RealUser
from wikinotes.models.pages import Page, PageType
from wikinotes.models.courses import Course, CourseSemester
from wikinotes.models.departments import Department
from wikinotes.models.professors import Professor
from wikinotes.forms.pages import PageForm
from wikinotes.utils.pages import get_max_num_sections
from django.template import RequestContext
import os

def view(request, department, number, term, year, page_type, slug):
	this_course = get_object_or_404(Course, department=department, number=int(number))
	this_type = get_object_or_404(PageType, slug=page_type)
	this_semester = "%s %s" % (term.title(), year)
	course_semester = get_object_or_404(CourseSemester, semester=this_semester, course=this_course)
	# Find the page attached to the slug the user entered
	this_page = get_object_or_404(Page, course_semester=course_semester, page_type=this_type, slug=slug)
	
	faculty = Department.objects.get(pk=department).faculty
	faculty_slug = faculty.slug
	
	num_sections = this_page.num_sections
	section_contents = []
	section_dirs = 'content/%s_%d/%s/%s' % (department, int(number), this_type.slug, this_page.slug)
	# Concatenate all of the files into a single string using a list comprehension (fastest method)
	for section_num in xrange(1, num_sections+1):
		filename = '%s/%d.md' % (section_dirs, section_num)
		file = open(filename, 'r')
		file_lines = file.readlines()
		section_contents.append(''.join([file_line for file_line in file_lines]))
	
	page_content = ''.join(section_content for section_content in section_contents)
	
	return render_to_response('page/view.html', locals())

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
	
	# The template name for what the input boxes etc should look like
	section_template = 'page/section-%s.html' % this_type.slug
	# For initially creating the hidden sections on the page
	# For better degradation if javascript is disabled
	num_sections = xrange(1, get_max_num_sections()+1)
	
	# If the form has been submitted, try to process it
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			# Add a preview mode later
			page = form.save(commit=False)
			page.page_type = this_type
			if page.subject == '':
				# The subject needs to be like Midterm or whatever
				page.subject = request.POST['exam_type']
			
			# If it needs a date, add it
			if this_type.need_date:
				page.date = '%s, %s %d' % (request.POST['weekday'], request.POST['month'], int(request.POST['day']))
			
			this_semester = "%s %s" % (request.POST['term'], request.POST['year'])
			# If the course semester doesn't already exist, create it with a ? for the prof
			try:
				course_semester = CourseSemester.objects.get(semester=this_semester, course=this_course)
			except CourseSemester.DoesNotExist:
				# Create a new one with an unknown prof (edit later)
				course_semester = CourseSemester(course=this_course, semester=this_semester)
				course_semester.save()
			page.course_semester = course_semester
			
			# Create the slug from, whatever
			page.slug = page.get_slug()[0]
			full_slug = page.get_slug()[1]
			
			# Save all the relevant pages (depending on the number of sections)
			sections_to_save = xrange(1, int(request.POST['num_sections'])+1)
			section_dirs = 'content/%s_%d/%s/%s' % (department, int(number), this_type.slug, page.slug)
			for section_num in sections_to_save:
				
				# Now save to a file
				# Ex: MATH_141/exam/[slug]
				section_file = '%s.md' % section_num
				try:
					os.makedirs(section_dirs)
					# First check if the git repository needs to be created first
					if not os.path.exists("%s/.git" % section_dirs):
						os.system("cd %s; git init" % section_dirs)
						
					filename = '%s/%s' % (section_dirs, section_file)
					file = open(filename, 'w')
					file.write(request.POST['section-%d-header' % section_num])
					file.write("\n===\n\n")
					file.write(request.POST['section-%d-content' % section_num])
					file.write("\n\n")
					file.close()
					os.system("cd %s; git add %s" % (section_dirs, section_file))
				except OSError:
					pass
			
			# Now save the model
			page.save()
			# Commit it lol
			# Of course this may STILL result in the non-atomicity issue but hopefully it will be less likely
			comment = request.POST['comment'] if request.POST['comment'] else 'Minor edit'
			# Escape quotation marks (should escape other things too probably to be safe)
			comment = comment.replace('"', '\\"')
			os.system('cd %s; git commit -m "%s"' % (section_dirs, comment))
			return render_to_response('page/success.html', locals())
		else:
			errors = ""
			for error in form.errors:
				errors = "%s %s: %s" % (errors, error, form.errors[error])
			return HttpResponse(errors)
	else:
		form = PageForm()
	
	return render_to_response('page/create.html', locals(), context_instance=RequestContext(request))
