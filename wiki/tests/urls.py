from django.contrib.auth.models import User
from django.test import TestCase

from wiki.models.courses import Course, CourseSemester, Professor
from wiki.models.departments import Department
from wiki.models.faculties import Faculty
from wiki.models.history import HistoryItem
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


class TestHistoryItemWithCommit(_TestGetAbsoluteUrl):
    expected = ('/MATH_150/summary/fall-2011/page-number-1/commit/'
                'e5b5d800710df83c530e9b38e87fbc55559135f9')

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
