from django.test import TestCase

from wiki.models.courses import Course
from wiki.models.pages import Page
from wiki.models.series import Series


class TestGetNextPosition(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.series = Series.objects.create(course=Course.objects.get(pk=1),
            name='new', position=2, slug='new')

    def test_empty_series(self):
        self.assertEqual(self.series.get_next_position(), 1)

    def test_nonempty_series(self):
        page_1 = Page.objects.get(pk=1)
        page_2 = Page.objects.get(pk=2)
        self.series.seriespage_set.create(page=page_1, position=1)
        self.assertEqual(self.series.get_next_position(), 2)
        self.series.seriespage_set.create(page=page_2, position=2)
        self.assertEqual(self.series.get_next_position(), 3)
