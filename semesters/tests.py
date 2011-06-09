from django.test import TestCase
from semesters.utils import get_possible_years

class TestSemesterShit(TestCase):
    def test_possible_years(self):
        """
        Test we get the correct list of possible years
        I can't really make the current year not hardcoded otherwise the test needs to be tested and yeah
        """
        self.failUnlessEqual([2010, 2011], get_possible_years())

