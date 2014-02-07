import itertools
import json
import random as random_module
import re

from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext

from wiki.forms.courses import CourseForm
from wiki.models.courses import Course, CourseSemester, Professor
from wiki.models.departments import Department
from wiki.models.faculties import Faculty
from wiki.models.history import HistoryItem
from wiki.models.pages import Page, ExternalPage
from wiki.models.series import Series
from wiki.utils.decorators import show_object_detail
from wiki.utils.pages import page_types


def remove_slash(request, department, number):
    """Replace a slash with an underscore.

    Example: math/133 --> math_133.
    """
    path = request.path_info
    real_path = path[:5] + '_' + path[6:]
    return redirect(real_path)


@show_object_detail(Faculty)
def faculty_overview(request, faculty):
    """Faculty overview page.
    """
    courses = Course.objects.all().filter(department__faculty=faculty)
    departments = faculty.department_set.all()

    return {
        'title': str(faculty),
        'faculty': faculty,
        'courses': courses,
        'departments': departments,
    }


@show_object_detail(Department)
def department_overview(request, dept):
    """Department overview page.
    """
    courses = dept.course_set.order_by('department__short_name', 'number')

    # Figure out the number of pages associated with courses in this department
    num_pages = Page.objects.filter(course_sem__course__department=dept).count()

    return {
        'title': str(dept),
        'dept': dept,
        'courses': courses,
        'num_pages': num_pages
    }


# Faculty no longer looks like a word to me
def faculty_browse(request):
    """Faculty listing page.
    """
    faculty_objects = Faculty.objects.all().order_by('name')
    courses = Course.objects
    faculties = []

    for faculty in faculty_objects:
        faculty_courses = courses.filter(department__faculty=faculty)
        faculties.append((faculty, faculty_courses))

    context = {
        'title': 'Browse by faculty',
        'faculties': faculties,
    }

    return render(request, 'courses/faculty_browse.html', context)


# Same pattern as faculty view
def department_browse(request):
    """Department listing page.
    """
    departments = Department.objects.all().order_by('long_name')

    context = {
        'title': 'Browse by department',
        'departments': departments,
    }

    return render(request, 'courses/department_browse.html', context)


def professor_browse(request):
    """Professor listing page.
    """
    professors = Professor.objects.all()
    context = {
        'professors': professors,
        'title': 'Browse by professor',
    }
    return render(request, 'courses/professor_browse.html', context)


def random(request):
    """Display a random course.
    """
    courses = Course.objects.all()
    random_course = random_module.choice(courses)
    return overview(request, random_course.department, random_course.number)


def index(request):
    """Main course listing page, at courses/.
    """
    courses = Course.objects.all()

    random_courses = random_module.sample(courses, 10)
    popular_courses = courses.filter(num_watchers__gt=0).order_by(
        '-num_watchers')[:10]
    active_courses = courses.filter(latest_activity__isnull=False).order_by(
        '-latest_activity__timestamp')[:10]
    num_courses = Page.objects.values('course_sem__course').distinct().count()
    num_departments = Page.objects.values('course_sem__course__department')\
                      .distinct().count()

    context = {
        'title': 'Courses',
        'random_courses': random_courses,
        'popular_courses': popular_courses,
        'active_courses': active_courses,
        'num_courses': num_courses,
        'num_departments': num_departments,
    }

    return render(request, 'courses/index.html', context)


def popular_browse(request):
    return all_browse(request, 'popularity')


def active_browse(request):
    return all_browse(request, 'activity')


def all_browse(request, sort_by=''):
    all_courses = Course.objects

    title = 'Browse courses by %s' % sort_by
    if sort_by == 'popularity':
        courses = all_courses.order_by('-num_watchers')
    elif sort_by == 'activity':
        active_courses = all_courses.filter(latest_activity__isnull=False)\
                        .order_by('-latest_activity__timestamp')
        inactive_courses = all_courses.filter(latest_activity__isnull=True)
        # Whoa.
        courses = itertools.chain(active_courses, inactive_courses)
    else:
        courses = all_courses.order_by('department', 'number')
        title = 'Browse all courses'

    context = {
        'title': title,
        'mode': sort_by,
        'courses': courses,
    }

    return render(request, 'courses/all_browse.html', context)


def watch(request, department, number):
    course = get_object_or_404(Course, department=department,
                               number=int(number))

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


@show_object_detail(Course)
def overview(request, course):
    # We can't use it directly in the template file, it just won't work
    types = []
    num_misc_pages = 0

    for name, obj in page_types.iteritems():
        # Get all the pages associated with this page type (and this course)
        pages = Page.objects.filter(page_type=name, course_sem__course=course,
                                    seriespage=None)
        external_pages = ExternalPage.objects.filter(page_type=name,
                                                     course=course)
        num_misc_pages += pages.count() + external_pages.count()
        pages = filter(lambda p: p.can_view(request.user), pages)
        type_data = {
            'name': name,
            'url': obj.get_create_url(course),
            'icon': obj.get_icon(),
            'long_name': obj.long_name,
            'desc': obj.description,
            'list_header': obj.get_list_header(),
            'list_body': obj.get_list_body(),
            'pages': pages,
            'external_pages': external_pages
        }
        types.append(type_data)

    # Get all the course semesters related to this course
    course_sems = CourseSemester.objects.filter(course=course)

    if request.user.is_authenticated():
        is_watching = request.user.get_profile().is_watching(course)
    else:
        is_watching = False

    return {
        'title': str(course),
        'is_watching': is_watching,
        'course': course,
        'page_types': types,
        'has_misc_pages': num_misc_pages > 0,
        'course_sems': course_sems,
        'current_sem': course.get_current_semester(),
        'visible_series': course.series_set.visible(request.user),
    }


# Filtering by semester for a specific course
@show_object_detail(CourseSemester)
def semester(request, course_sem):
    course = course_sem.course
    pages = Page.objects.visible(request.user, course_sem=course_sem)

    return {
        'title': course_sem,
        'course': course,
        'course_sem': course_sem,
        'pages': pages,
    }


def recent(request, department, number):
    course = get_object_or_404(Course, department=department,
                               number=int(number))
    raw_history = course.recent_activity(limit=0) # order: newest to oldest
    temp_history = []

    # First pass - collapse all watchings by the same user into one event
    # Only keep the earliest one
    users_watching = []
    for item in reversed(raw_history):
        # This is actually pretty bad
        if item.action == 'started watching' and item.user in users_watching:
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

        # Second pass - combine multiple consecutive edits into one, use latest
        for item in temp_history[1:]:
            last_item = history[-1]

            # If the last action was an edit by the same user, on the same pag:
            if (item.action == last_item.action == 'edited' and
                item.page == last_item.page != None and
                item.user == last_item.user):
                last_item.group_count += 1
            elif item.action == last_item.action == 'started watching':
                # Otherwise, if the last action was also a watch:
                last_item.group_count += 1
                last_item.action += ' this course'
            else:
                # Only append if you can't group
                history.append(item)
                if item.action == 'started watching':
                    item.action += ' this course'

    return {
        'title': 'Recent activity for %s' % course,
        'course': course,
        'history': reversed(history) # reverse it again to get the right order
    }


@show_object_detail(Course, always_pass_groups=True)
def category_overview(request, course, **kwargs):
    page_type = kwargs['page_type']

    if page_type not in page_types:
        raise Http404

    pages = Page.objects.visible(request.user, course_sem__course=course,
                                 page_type=page_type)
    category = page_types[page_type]

    return {
        'title': '%s content for %s' % (category.long_name, course),
        'course': course,
        'category': category,
        'pages': pages,
        'create_url': category.get_create_url(course),
    }


@show_object_detail(Professor)
def professor_overview(request, professor):
    pages = Page.objects.visible(request.user, professor=professor)\
            .order_by('course_sem')

    return {
        'title': 'Overview for %s' % professor,
        'professor': professor,
        'pages': pages,
    }


def create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save()
            return redirect(course)
    else:
        form = CourseForm()

    context = {
        'title': 'Create a course',
        'form': form,
    }

    return render(request, 'courses/create.html', context)
