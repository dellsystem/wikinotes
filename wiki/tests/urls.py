from django.test import TestCase

from wiki.models.courses import Course, CourseSemester, Professor
from wiki.models.departments import Department
from wiki.models.faculties import Faculty
from wiki.models.pages import Page
from wiki.models.series import Series
from wiki.models.users import PrivateMessage, UserProfile


class _TestGetAbsoluteUrl(TestCase):
    """Parent class for testing the get_absolute_url() method on the models
    that define it. Subclass this.
    """
    fixtures = ['test']
    pk = 1

    def setUp(self):
        # Take the object with the defined primary key (defaults to 1)
        self.obj = self.model.objects.get(pk=self.pk)

    def runTest(self):
        self.assertEqual(self.expected, self.obj.get_absolute_url())


class TestCourse(_TestGetAbsoluteUrl):
    expected = '/MATH_150/'
    model = Course


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


class TestFaculty(_TestGetAbsoluteUrl):
    expected = '/faculty/science/'
    model = Faculty


class TestPage(_TestGetAbsoluteUrl):
    expected = '/MATH_150/summary/fall-2011/page-number-1/'
    model = Page


class TestSeries(_TestGetAbsoluteUrl):
    expected = '/MATH_150/#series-fall-2010-lecture-notes'
    model = Series
