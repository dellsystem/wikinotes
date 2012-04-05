from django.shortcuts import render, get_object_or_404, redirect
from wiki.models.courses import Course, CourseSemester
from wiki.utils.constants import terms, years, exam_types
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
from datetime import datetime


def show(request, department, number, page_type, term, year, slug):
	try:
		course = get_object_or_404(Course, department=department, number=int(number))
	except Http404:
		return render(request, "courses/404.html", {'department': department, 'number': number})
	try:
		course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
		page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	except Http404:
		# Page doesn't exist - go to create with the semester, subject, etc filled out
		return create(request, department, number, page_type, semester=(term, year))

	page_type_obj = page_types[page_type]
	data = {
		'title': '%s (%s)' % (page, course),
		'course': course,
		'page': page,
		'page_type': page_type_obj,
		'content': page.load_content(),
		'edit_url': page.get_absolute_url() + '/edit',
		'history_url': page.get_absolute_url() + '/history',
	}
	return render(request, "pages/show.html", data)

def history(request, department, number, page_type, term, year, slug):
	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	commit_history = Git(page.get_filepath()).get_history()
	data = {
		'title': 'Page history (%s)' % page,
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
	repo = Git(page.get_filepath()) # make this an object on the page
	commit = repo.get_commit(hash)
	files = {}
	for blob in commit.tree:
		raw = blob.data_stream.read().split('\n')
		files[blob.name] = {
			'raw': '\n'.join(raw),
			'title': raw[0].strip(),
			'data': page_type_obj.format(raw[3:]),
		}

	raw_file = files.items()[0][1]['raw']

	previous = repo.get_previous(commit)
	if previous:
		diff_lines = previous.diff(commit.hexsha, create_patch=True)[0].diff.splitlines()[2:]
		diff_info = diff_lines[0].split(' ')
		diff_before = diff_info[1].split(',')
		diff_after = diff_info[2].split(',')
		diff = {'first_line': diff_before[0][1:], 'lines_before': diff_before[1], 'lines_after': diff_after[1], 'lines': [' '.join(diff_info[4:])] + diff_lines[3:]}
	else:
		diff = None

	data = {
		'title': 'Commit information (%s)' % page,
		'course': course,
		'page': page,
		'hash': hash,
		'content': raw_file,
		'commit': {
			'date': datetime.fromtimestamp(commit.authored_date), # returns a unix timestamp in 0.3.2
			'author': User.objects.get(username=commit.author.name),
			'message': commit.message,
			'stats': commit.stats.total,
			'diff': diff
		},
	}

	return render(request, "pages/commit.html", data)
def edit(request, department, number, page_type, term, year, slug):
	if not request.user.is_authenticated():
		return register(request)

	if page_type not in page_types:
		raise Http404

	course = get_object_or_404(Course, department=department, number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=year)
	page = get_object_or_404(Page, course_sem=course_sem, page_type=page_type, slug=slug)
	page_type_obj = page_types[page_type]

	if request.method == 'POST':
		# Just do save sections with the data
		username = request.user.username
		message = request.POST['message']
		page.save_content(request.POST['content'], message, username)
		data = {
			'course': course,
			'page': page,
		}

		# Only change the metadata if the user is a moderator
		if request.user.is_staff:
			page.edit(request.POST)

		# Add the history item
		course.add_event(page=page, user=request.user, action='edited', message=message)
		return redirect(page.get_absolute_url())

	field_templates = page_type_obj.get_editable_fields()
	non_field_templates = ['pages/%s_data.html' % field for field in page_type_obj.editable_fields]

	data = {
		'title': 'Edit (%s)' % page,
		'course': course,
		'page': page,
		# ONLY SHOW THE BELOW FOR MODERATORS (once that is implemented)
		'field_templates': field_templates if request.user.is_staff else non_field_templates,
		'page_type': page_type_obj,
		'content': page.load_content(),
		'subject': page.subject,
		'exam_types': exam_types,
	}
	return render(request, "pages/edit.html", data)

# semester should only be filled out if the page doesn't exist and we want to create it
def create(request, department, number, page_type, semester=None):
	if not request.user.is_authenticated():
		return register(request)

	course = get_object_or_404(Course, department=department, number=int(number))

	if page_type not in page_types:
		raise Http404

	page_type_obj = page_types[page_type]
	data = {
		'title': 'Create a page (%s)' % course,
		'course': course,
		'page_type': page_type_obj,
		'terms': terms,
		'field_templates': page_type_obj.get_uneditable_fields() + page_type_obj.get_editable_fields(),
		'years': years,
		'page_type_url': page_type_obj.get_url(course), # can't call it on page_type_obj directly
		'current_term': current_term,
		'current_year': current_year,
		'exam_types': exam_types,
		'current_exam_type': exam_types[0], # default
		'edit_mode': False,
	}

	if semester is not None:
		data['current_term'] = semester[0]
		data['current_year'] = int(semester[1])
		data['does_not_exist'] = True

	if request.method == 'POST':
		errors = page_type_obj.find_errors(request.POST)
		kwargs = page_type_obj.get_kwargs(request.POST)
		course_sem, created = CourseSemester.objects.get_or_create(term=request.POST['term'], year=request.POST['year'], course=course)
		is_unique = Page.objects.filter(course_sem=course_sem, slug=kwargs['slug']).count() == 0
		if errors or not is_unique: # it returns None only if nothing is wrong
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
			data['subject'] =  request.POST['subject'] if 'subject' in request.POST else ''

			data['content'] = request.POST['content']
			data['message'] = request.POST['message']

			return render(request, 'pages/create.html', data)
		else:
			commit_message = request.POST['message']
			# The title and subject are generated by the PageType object, in kwargs
			new_page = Page(course_sem=course_sem, page_type=page_type, **kwargs)
			new_page.save()
			username = request.user.username
			email = request.user.email
			new_page.save_content(request.POST['content'], commit_message, username)

			# Add the history item - should be done automatically one day
			course.add_event(page=new_page, user=request.user, action='created', message=commit_message)
			data['page'] = new_page
			return redirect(new_page.get_absolute_url())

	return render(request, 'pages/create.html', data)

def random(request):
	pages = Page.objects.all()
	random_page = random_module.choice(pages)
	return show(request, random_page.course_sem.course.department, random_page.course_sem.course.number, random_page.page_type, random_page.course_sem.term, random_page.course_sem.year, random_page.slug)
