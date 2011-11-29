from django.shortcuts import render, get_object_or_404
from wiki.models.courses import Course, CourseSemester
from wiki.utils.constants import terms, years, exam_types, max_num_sections
from wiki.utils.gitutils import Git
from wiki.utils.pages import page_types
from django.template import RequestContext
from wiki.models.pages import Page
from django.http import Http404
import random as random_module
from wiki.models.history import HistoryItem
from django.contrib.auth.models import User
from wiki.utils.currents import current_term, current_year
from views.main import register

def show(request, department, number, page_type, term, year, slug):
	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	page_type_obj = page_types[page_type]
	data = {
		'course': course,
		'page': page,
		'sections': page.load_sections(),
		'show_template': page_type_obj.get_show_template(),
		'edit_url': page.get_url() + '/edit',
		'history_url': page.get_url() + '/history',
	}
	return render(request, "pages/show.html", data)

def history(request, department, number, page_type, term, year, slug):
	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	commit_history = Git(page.get_filepath()).get_history()
	data = {
		'course': course,
		'page': page, # to distinguish it from whatever
		'commit_history': commit_history,
	}
	return render(request, "pages/history.html", data)

# View page information for a specific commit
def commit(request, department, number, page_type, term, year, slug, hash):
	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	page_type_obj = page_types[page_type]
	commit = Git(page.get_filepath()).get_commit(hash)
	files = {}
	for blob in commit.tree:
		raw = blob.data_stream.read().split('\n')
		files[blob.name] = {
			'raw': '\n'.join(raw),
			'title': raw[0].strip(),
			'data': page_type_obj.format(raw[3:]),
		}

	data = {
		'course': course,
		'page': page,
		'hash': hash,
		'show_template': page_type_obj.get_show_template(),
		'commit': {
			'author': User.objects.get(username=commit.author.name),
			'message': commit.message,
			'stats': commit.stats.total,
			'files': files
		},
		'sections': files
	}

	return render(request, "pages/commit.html", data)
def edit(request, department, number, page_type, term, year, slug):
	if page_type not in page_types:
		raise Http404

	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	page_type_obj = page_types[page_type]

	if request.method == 'POST':
		# Just do save sections with the data
		username = request.user.username if request.user.is_authenticated() else 'Anonymous'
		email = request.user.email if request.user.is_authenticated() else 'example@example.com'
		page.save_sections(request.POST, username, email)
		data = {
			'course': course,
			'page': page,
		}

		# The page may need changing ...
		page.edit(request.POST)

		# Add the history item
		course.add_event(page=page, user=request.user, action='edited', message=request.POST['message'])
		return render(request, "pages/success.html", data)

	data = {
		'course': course,
		'page': page, # to distinguish it from whatever
		'field_templates': page_type_obj.get_field_templates(),
		'num_sections': range(1, 11),
		'help_template': page_type_obj.get_help_template(),
		'sections': page.load_sections(),
		'num_sections': range(1, 11) if page.num_sections < 11 else range(1, page.num_sections + 1), # check on this later
		'terms': ['winter', 'summer', 'fall'], # fix this later
		'years': range(2011, 1999, -1),
	}
	return render(request, "pages/edit.html", data)

def create(request, department, number, page_type):
	return create_or_edit(request, department, number, page_type)

def create_or_edit(request, department, number, page_type, term=current_term, year=current_year, slug=None):
	if not request.user.is_authenticated():
		return register(request)

	course = get_object_or_404(Course, department=department, number=int(number))

	if page_type not in page_types:
		raise Http404

	page_type_obj = page_types[page_type]
	sections = [{'i': i, 'id': 'section-%d' % i, 'title': '', 'body': ''} for i in xrange(1, max_num_sections + 1)]
	data = {
		'course': course,
		'page_type': page_type_obj,
		'terms': terms,
		'field_templates': page_type_obj.get_field_templates(),
		'years': years,
		'current_term': term,
		'current_year': year,
		'sections': sections,
		'exam_types': exam_types,
		'current_exam_type': exam_types[0], # default
	}

	if slug:
		# Edit
		course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
		data['page'] = get_object_or_404(Page, course_sem=course_sem, page_type=page_type_obj, slug=slug)
		data['current_exam'] = page.exam_type

	if request.method == 'POST':
		errors = page_type_obj.find_errors(request.POST)
		kwargs = page_type_obj.get_kwargs(request.POST)
		is_unique = Page.objects.get(course_sem=course_sem, slug=kwargs['slug']).count() == 0
		if errors is not None or not is_unique: # it returns None only if nothing is wrong
			data['errors'] = errors
			if not is_unique:
				data['errors'].append('Subject or whatever not unique') # Fix this later
			# Keep the posted data
			data['current_term'] = request.POST['term']
			try:
				data['current_year'] = int(request.POST['year'])
			except ValueError:
				pass # defaults to the current year
			data['current_exam_type'] = request.POST['exam_type'] if 'exam_type' in request.POST else ''
			data['subject'] =  request.POST['subject']

			# Find a better way to do this
			for i in xrange(1, max_num_sections):
				section_title = "section-%d-title" % i
				section_body = "section-%d-body" % i
				data['sections'][i-1]['title'] = request.POST[section_title]
				data['sections'][i-1]['body'] = request.POST[section_body]

			return render(request, 'pages/create_edit.html', data)
		else:
			if not slug:
				course_sem, created = CourseSemester.objects.get_or_create(term=term, year=year, course=course)

				# The title and subject are generated by the PageType object, in kwargs
				new_page = Page(course_sem=course_sem, page_type=page_type, **kwargs)
				new_page.save()
				username = request.user.username
				email = request.user.email
				new_page.save_sections(request.POST, username, email, num_sections=kwargs['num_sections'])

				# Add the history item - should be done automatically one day
				course.add_event(page=new_page, user=request.user, action='created', message=request.POST['message'])
				data['page'] = new_page
				return render(request, "pages/success.html", data)

	return render(request, 'pages/create_edit.html', data)

"""
def create(request, department, number, page_type):
	course = get_object_or_404(Course, department=department, number=int(number))

	if page_type not in page_types:
		raise Http404
	else:
		obj = page_types[page_type]
		if request.method == 'POST':
			# Create the page
			num_sections = request.POST['num_sections']
			term = request.POST['term']
			year = request.POST['year']
			try:
				course_sem = CourseSemester.objects.get(term=term, year=year, course=course)
			except CourseSemester.DoesNotExist:
				course_sem = CourseSemester(term=term, year=year, course=course)
				course_sem.save()

			# The title and subject are generated by the PageType object, in kwargs
			kwargs = obj.get_kwargs(request.POST)
			new_page = Page(course_sem=course_sem, num_sections=num_sections, page_type=page_type, **kwargs)
			new_page.save()
			username = request.user.username if request.user.is_authenticated() else 'Anonymous'
			email = request.user.email if request.user.is_authenticated() else 'example@example.com'
			new_page.save_sections(request.POST, username, email)
			data = {
				'course': course,
			}

			# Add the history item
			course.add_event(page=new_page, user=request.user, action='created', message=request.POST['message'])

			# Get the keyword arguments from the page type method
			if new_page:
				data['page'] = new_page
				return render(request, "pages/success.html", data)
			else:
				return render(request, "pages/error.html", data)
		else:
			data = {
				'course': course,
				'page_type': obj,
				'form_template': obj.get_form_template(),
				'help_template': obj.get_help_template(),
				'field_templates': obj.get_field_templates(),
				'terms': ['winter', 'summer', 'fall'], # fix this later
				'years': range(2011, 1999, -1),
				'num_sections': range(1, 11), # for people without javascript DON'T DELETE THIS UNLESS YOU HAVE ANOTHER SOLUTION FOR A FALLBACK
			}
			return render(request, "pages/create.html", data)
"""
def random(request):
	pages = Page.objects.all()
	random_page = random_module.choice(pages)
	return show(request, random_page.course_sem.course.department, random_page.course_sem.course.number, random_page.page_type, random_page.course_sem.term, random_page.course_sem.year, random_page.slug)
