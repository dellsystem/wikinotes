from django.contrib.auth.models import User
from django.test import TestCase

from wiki.models.courses import Course, CourseSemester, Professor
from wiki.models.departments import Department
from wiki.models.faculties import Faculty
from wiki.models.history import HistoryItem
from wiki.models.pages import Page
from wiki.models.series import Series
from wiki.models.users import PrivateMessage, UserProfile
from wiki.utils.pages import page_types


class _TestGetAbsoluteUrl(TestCase):
    """Parent class for testing the get_absolute_url() method on the models
    that define it. Subclass this. Override method_name to test a method named
    something other than get_absolute_url().
    """
    fixtures = ['test']
    pk = 1
    method_name = 'get_absolute_url'
    args = []

    def setUp(self):
        # Take the object with the defined primary key (defaults to 1)
        self.obj = self.model.objects.get(pk=self.pk)

    def runTest(self):
        self.assertEqual(self.expected,
            getattr(self.obj, self.method_name)(*self.args))


class TestCourse(_TestGetAbsoluteUrl):
    expected = '/MATH_150/'
    model = Course


class TestCourseRecentUrl(_TestGetAbsoluteUrl):
    expected = '/MATH_150/recent/'
    model = Course
    method_name = 'get_recent_url'


class TestCourseWatchUrl(_TestGetAbsoluteUrl):
    expected = '/MATH_150/watch/'
    model = Course
    method_name = 'get_watch_url'


class TestCourseSemester(_TestGetAbsoluteUrl):
    expected = '/MATH_150/fall-2011/'
    model = CourseSemester


class TestProfessor(_TestGetAbsoluteUrl):
    expected = '/professor/james-loveys/'
    model = Professor


class TestDepartment(_TestGetAbsoluteUrl):
    expected = '/MATH/'
    model = Department
    pk = "MATH"


class TestDepartmentImage(TestDepartment):
    expected = '/static/img/department/MATH.png'
    method_name = 'get_image'


class TestDepartmentLargeImage(TestDepartment):
    expected = '/static/img/department/MATH_large.png'
    method_name = 'get_large_image'


class TestFaculty(_TestGetAbsoluteUrl):
    expected = '/faculty/science/'
    model = Faculty


class TestFacultyImage(TestFaculty):
    expected = '/static/img/faculty/science.png'
    method_name = 'get_image'


class TestPage(_TestGetAbsoluteUrl):
    expected = '/MATH_150/summary/fall-2011/page-number-1/'
    model = Page


class TestPageHistoryUrl(_TestGetAbsoluteUrl):
    expected = '/MATH_150/summary/fall-2011/page-number-1/history/'
    model = Page
    method_name = 'get_history_url'


class TestPagePrintUrl(_TestGetAbsoluteUrl):
    expected = '/MATH_150/summary/fall-2011/page-number-1/print/'
    model = Page
    method_name = 'get_print_url'


class TestPageEditUrl(_TestGetAbsoluteUrl):
    expected = '/MATH_150/summary/fall-2011/page-number-1/edit/'
    model = Page
    method_name = 'get_edit_url'


class TestSeries(_TestGetAbsoluteUrl):
    expected = '/MATH_150/#series-fall-2010-lecture-notes'
    model = Series


class TestHistoryItemWithCommit(_TestGetAbsoluteUrl):
    expected = ('/MATH_150/summary/fall-2011/page-number-1/commit/'
                'e5b5d800710df83c530e9b38e87fbc55559135f9/')

    def setUp(self):
        """The object is not in the fixtures, so we have to create it first."""
        self.obj = HistoryItem.objects.create(
            user=User.objects.get(pk=1),
            action='edited',
            page=Page.objects.get(pk=1),
            course=Course.objects.get(pk=1),
            hexsha='e5b5d800710df83c530e9b38e87fbc55559135f9')


class TestHistoryItemWithPage(_TestGetAbsoluteUrl):
    expected = '/MATH_150/summary/fall-2011/page-number-1/history/'

    def setUp(self):
        self.obj = HistoryItem.objects.create(
            user=User.objects.get(pk=1),
            action='created',
            page=Page.objects.get(pk=1),
            course=Course.objects.get(pk=1))


class TestHistoryItemWithCourse(_TestGetAbsoluteUrl):
    expected = '/MATH_150/recent/'

    def setUp(self):
        self.obj = HistoryItem.objects.create(
            user=User.objects.get(pk=1),
            action='started watching',
            course=Course.objects.get(pk=1))


class TestPageTypeUrl(_TestGetAbsoluteUrl):
    expected = '/MATH_150/summary/'
    method_name = 'get_url'

    def setUp(self):
        self.obj = page_types['summary']
        self.args = [Course.objects.get(pk=1)]


class TestPageTypeCreateUrl(_TestGetAbsoluteUrl):
    expected = '/MATH_150/create/summary/'
    method_name = 'get_create_url'

    def setUp(self):
        self.obj = page_types['summary']
        self.args = [Course.objects.get(pk=1)]
