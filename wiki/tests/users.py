from django.contrib.auth.models import User
from django.test import TestCase

from wiki.models.users import UserProfile
from wiki.models.pages import Page
from wiki.models.history import HistoryItem
from wiki.models.courses import Course


class TestUserProfile(TestCase):
    fixtures = ['faculties', 'departments', 'courses', 'professors', 'coursesemesters', 'test_pages']

    def setUp(self):
        self.user = User.objects.create_user('lol')
        self.profile = self.user.get_profile()

    def test_get_recent_pages(self):
        pages = Page.objects.all()
        course = Course.objects.get(pk=1)

        # First, edit page 1 twice
        HistoryItem.objects.create(user=self.user, action='edited', page=pages[0], course=course)
        HistoryItem.objects.create(user=self.user, action='edited', page=pages[0], course=course)
        # Then edit page 2 once
        HistoryItem.objects.create(user=self.user, action='edited', page=pages[1], course=course)
        # Then edit page 4 once
        HistoryItem.objects.create(user=self.user, action='edited', page=pages[3], course=course)
        # Then edit page 2 once
        HistoryItem.objects.create(user=self.user, action='edited', page=pages[1], course=course)
        # Then edit page 3 once
        HistoryItem.objects.create(user=self.user, action='edited', page=pages[2], course=course)

        self.assertEqual(self.profile.get_recent_pages(5), [pages[2], pages[1], pages[3], pages[0]])
        self.assertEqual(self.profile.get_recent_pages(3), [pages[2], pages[1], pages[3]])

    def tearDown(self):
        self.user.delete()

    def test_username(self):
        self.assertEqual(self.user.username, 'lol')
