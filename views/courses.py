from django.shortcuts import render, get_object_or_404, redirect
from wiki.models.courses import Course, CourseSemester
from wiki.models.faculties import Faculty
from wiki.models.departments import Department
from wiki.models.series import Series
from wiki.utils.pages import page_types
from django.template import RequestContext
from wiki.models.pages import Page
import random as random_module
from wiki.models.history import HistoryItem
from django.http import Http404
import re
import json
from itertools import chain

# Remove the slash and replace it with an underscore. math/133 --> math_133
def remove_slash(request, department, number):
	path = request.path_info
	real_path = path[:5] + '_' + path[6:]
	return redirect(real_path)

def faculty_overview(request, faculty):
	faculty_object = get_object_or_404(Faculty, slug=faculty)
	courses = Course.objects.all().filter(department__faculty=faculty_object).order_by('department__short_name', 'number')
	departments = Department.objects.all().filter(faculty=faculty_object).order_by('short_name')
	data = {
		'title': faculty_object,
		'faculty': faculty_object,
		'courses': courses,
		'departments': departments
	}
	return render(request, 'courses/faculty_overview.html', data)

def department_overview(request, department):
	dept = get_object_or_404(Department, short_name=department.upper())
	courses = Course.objects.all().filter(department=dept).order_by('department__short_name', 'number')
	# Figure out the number of pages associated with courses in this department
	num_pages = Page.objects.filter(course_sem__course__department=dept).count()
	data = {
		'title': dept,
		'dept': dept,
		'courses': courses,
		'num_pages': num_pages
	}
	return render(request, 'courses/department_overview.html', data)

# Faculty no longer looks like a word to me
def faculty_browse(request):
	faculty_objects = Faculty.objects.all().order_by('name')
	courses = Course.objects.all()
	faculties = []

	for faculty in faculty_objects:
		faculty_courses = courses.filter(department__faculty=faculty).order_by('department__short_name', 'number')
		faculties.append({'name': faculty.name, 'slug': faculty.slug, 'courses': faculty_courses})

	data = {
		'title': 'Browse by faculty',
		'faculties': faculties,
	}

	return render(request, 'courses/faculty_browse.html', data)

# Same pattern as faculty view
def department_browse(request):
	department_objects = Department.objects.all().order_by('long_name')
	courses = Course.objects.all()
	departments = []

	for department in department_objects:
		department_courses = courses.filter(department=department).order_by('department__short_name', 'number')
		departments.append({'long': department.long_name, 'short': department.short_name, 'courses': department_courses})

	data = {
		'title': 'Browse by department',
		'departments': departments,
	}

	return render(request, 'courses/department_browse.html', data)

# Meh
def professor(request):
	return render(request, 'courses/professor.html', {'title': 'Browse by professor'})

def random(request):
	courses = Course.objects.all()
	random_course = random_module.choice(courses)
	return overview(request, random_course.department, random_course.number)

def index(request):
	courses = Course.objects.all()

	random_courses = random_module.sample(courses, 10)
	popular_courses = courses.filter(num_watchers__gt=0).order_by('-num_watchers')[:10]
	active_courses = courses.filter(latest_activity__isnull=False).order_by('-latest_activity__timestamp')[:10]

	data = {
		'title': 'Courses',
		'random_courses': random_courses,
		'popular_courses': popular_courses,
		'active_courses': active_courses,
		'num_courses': Page.objects.values('course_sem__course').distinct().count(),
		'num_departments': Page.objects.values('course_sem__course__department').distinct().count()
	}
	return render(request, 'courses/index.html', data)

def popular(request):
	return list_all(request, 'popularity')

def active(request):
	return list_all(request, 'activity')

def list_all(request, sort_by=''):
	all_courses = Course.objects

	if sort_by == 'popularity':
		courses = all_courses.order_by('-num_watchers')
	elif sort_by == 'activity':
		courses = chain(all_courses.filter(latest_activity__isnull=False).order_by('-latest_activity__timestamp'), all_courses.filter(latest_activity__isnull=True))
	else:
		courses = all_courses.order_by('department', 'number')

	data = {
		'title': 'Courses by %s' % sort_by,
		'mode': sort_by,
		'courses': courses,
	}
	return render(request, 'courses/all.html', data)

def watch(request, department, number):
	course = get_object_or_404(Course, department=department.upper(), number=int(number))

	if request.method == 'POST' and request.user.is_authenticated():
		user = request.user.get_profile()
		# If the user is already watching it, unwatch
		if user.is_watching(course):
			user.stop_watching(course)
		else:
			# Else, watch
			user.start_watching(course)

	return overview(request, department, number)

def get_all(request):
	courses = Course.objects.order_by('department', 'number')
	return render(request, 'courses/get_all.html', {'courses': courses})

def overview(request, department, number):
	try:
		course = get_object_or_404(Course, department=department.upper(), number=int(number))
	except Http404:
		return render(request, "courses/404.html", {'department': department.upper(), 'number': number})

	# We can't use it directly in the template file, it just won't work
	types = []
	for name, obj in page_types.iteritems():
		# Get all the pages associated with this page type (and this course etc)
		pages = Page.objects.filter(page_type=name, course_sem__course=course)
		types.append({'name': name, 'url': obj.get_create_url(course), 'icon': obj.get_icon(), 'long_name': obj.long_name, 'desc': obj.description, 'list_header': obj.get_list_header(), 'list_body': obj.get_list_body(), 'pages': pages})

	try:
		this_sem = CourseSemester.objects.get(course=course, term='winter', year='2011')
		this_sem_pages = this_sem.page_set.all()
	except CourseSemester.DoesNotExist:
		this_sem_pages = []

	# Get all the course semesters related to this course
	course_sems = CourseSemester.objects.filter(course=course)
	# Get all of the pages associated with this course (can't just do page_set because the foreign key is CourseSemester lol)
	all_pages = Page.objects.filter(course_sem__course=course)
	data = {
		'title': course,
		'is_watching': request.user.get_profile().is_watching(course) if request.user.is_authenticated() else False,
		'course': course,
		'page_types': types,
		'all_pages': all_pages,
		'this_sem_pages': this_sem_pages,
		'course_sems': course_sems,
		'current_sem': course.get_current_semester(),
	}
	return render(request, 'courses/overview.html', data)

# Filtering by semester for a specific course
def semester(request, department, number, term, year):
	course = get_object_or_404(Course, department=department.upper(), number=int(number))
	course_sem = get_object_or_404(CourseSemester, course=course, term=term, year=int(year))
	pages = Page.objects.filter(course_sem=course_sem)

	data = {
		'title': course_sem,
		'course': course,
		'course_sem': course_sem,
		'pages': pages,
	}

	return render(request, 'courses/semester.html', data)

def recent(request, department, number):
	course = get_object_or_404(Course, department=department.upper(), number=int(number))
	raw_history = course.recent_activity(limit=0) # order: newest to oldest
	temp_history = []

	# First pass - collapse all watchings by the same user into one event
	# Only keep the earliest one
	users_watching = []
	for item in reversed(raw_history):
		if item.action == 'started watching' and item.user in users_watching: # awful lol
			continue
		else:
			item.group_count = 0
			temp_history.append(item)
			if item.action == 'started watching':
				users_watching.append(item.user)

	history = []

	# Add the first one
	if temp_history:
		history.append(temp_history[0])

		# Second pass - combine multiple consecutive edits into one, use the latest
		for item in temp_history[1:]:
			last_item = history[-1]
			# If the last action was an edit by the same user, on the same page:
			if item.action == last_item.action == 'edited' and item.page == last_item.page != None and item.user == last_item.user:
				last_item.group_count += 1
			# Otherwise, if the last action was also a watch:
			elif item.action == last_item.action == 'started watching':
				last_item.group_count += 1
				last_item.action += ' this course'
			else:
				# Only append if you can't group
				history.append(item)
				if item.action == 'started watching':
					item.action += ' this course'

	data = {
		'title': '%s (Recent activity)' % course,
		'course': course,
		'history': reversed(history) # have to reverse it again to get the right order
	}

	return render(request, 'courses/recent.html', data)

def series(request, department, number, slug):
	course = get_object_or_404(Course, department=department.upper(), number=int(number))
	series = get_object_or_404(Series, course=course, slug=slug)

	data = {
		'title': series,
		'course': course,
		'series': series,
	}

	return render(request, 'courses/series.html', data)

def category(request, department, number, page_type):
	course = get_object_or_404(Course, department=department.upper(), number=int(number))
	if page_type not in page_types:
		raise Http404
	else:
		category = page_types[page_type]
		data = {
			'title': '%s (%s)' % (category.long_name, course),
			'course': course,
			'category': category,
			'pages': Page.objects.filter(course_sem__course=course, page_type=page_type),
			'create_url': category.get_create_url(course),
		}
		return render(request, 'courses/category.html', data)
