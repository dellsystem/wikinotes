from django.shortcuts import render, get_object_or_404
from wiki.models.courses import Course, CourseSemester
from wiki.models.faculties import Faculty
from wiki.models.departments import Department
from utils import page_types as types
from django.template import RequestContext
from wiki.models.pages import Page
import random as random_module
from wiki.models.history import HistoryItem

def faculty_overview(request, faculty):
	faculty_object = get_object_or_404(Faculty, slug=faculty)
	faculty_courses = Course.objects.all().filter(department__faculty=faculty_object).order_by('department__short_name', 'number')
	data = {
		'faculty': faculty_object,
		'courses': faculty_courses,
	}
	return render(request, 'courses/faculty_overview.html', data)

def department_overview(request, department):
	dept = get_object_or_404(Department, short_name=department)
	courses = Course.objects.all().filter(department=dept).order_by('department__short_name', 'number')
	data = {
		'dept': dept,
		'courses': courses,
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
		'departments': departments,
	}

	return render(request, 'courses/department_browse.html', data)

# Not really sure how to best implement this lol
def semester(request):
	return render(request, 'courses/semester.html')

# Meh
def professor(request):
	return render(request, 'courses/professor.html')

def popular(request):
	return render(request, 'courses/popular.html')

def random(request):
    courses = Course.objects.all()
    random_course = random_module.choice(courses)
    return overview(request, random_course.department, random_course.number)

def active(request):
	pass

def search(request):
	pass

def index(request):
	courses = Course.objects.all()

	random_courses = random_module.sample(courses, 5)
	popular_courses = courses.order_by('-watchers')[:5]
	active_courses = list(set([hist.course for hist in HistoryItem.objects.all().order_by('-timestamp')]))[:5] # lol order doesn't matter who cares about that

	data = {
		'random_courses': random_courses,
		'popular_courses': popular_courses,
		'active_courses': active_courses,
	}
	return render(request, 'courses/index.html', data)

def all(request):
	courses = Course.objects.all().order_by('department', 'number')
	data = {
		'courses': courses,
	}
	return render(request, 'courses/all.html', data)

def watch(request, department, number):
	course = get_object_or_404(Course, department=department, number=int(number))

	if request.method == 'POST' and request.user.is_authenticated():
		# If the user is already watching it, unwatch
		if course.has_watcher(request.user):
			# These really should be methods on the user but attempts to extend the user model are not working at the moment
			course.remove_watcher(request.user)
		else:
			# Else, watch
			course.add_watcher(request.user)

	return overview(request, department, number)

def overview(request, department, number):
	course = get_object_or_404(Course, department=department, number=int(number))

	# We can't use it directly in the template file, it just won't work
	page_types = []
	for name, obj in types.iteritems():
		# Get all the pages associated with this page type (and this course etc)
		pages = Page.objects.filter(page_type=name, course_sem__course=course)
		page_types.append({'name': name, 'url': obj.get_create_url(course), 'icon': obj.get_icon(), 'long_name': obj.long_name, 'desc': obj.description, 'show_template': obj.get_show_template(), 'list_template': obj.get_list_template(), 'pages': pages})

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
		'is_watching': course.has_watcher(request.user),
		'course': course,
		'page_types': page_types,
		'all_pages': all_pages,
		'this_sem_pages': this_sem_pages,
		'course_sems': course_sems,
	}
	return render(request, 'courses/overview.html', data)
