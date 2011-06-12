"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from wikinotes.utils.semesters import get_current_semester
from wikinotes.models.semesters import Semester
from wikinotes.models.pages import this_semester

class SimpleTest(TestCase):
    def test_current_semester(self):
    	semester_tuple = get_current_semester()
    	self.assertEqual(semester_tuple[0], 'Summer')
    	self.assertEqual(semester_tuple[1], 2011)
    def test_this_semester(self):
    	semester = this_semester()
    	real_semester = Semester.objects.get(term='Summer', year=2011)
    	self.assertEqual(semester, real_semester)
