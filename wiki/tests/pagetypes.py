from django.test import TestCase

from wiki.utils.pages import page_types


class _TestPageType(TestCase):
    """Parent class for testing various methods on the PageType subclasses."""
    def setUp(self):
        self.page_type = page_types[self.short_name]

    def test_slug(self):
        generated_slug = self.page_type._generate_slug(self.data)
        self.assertEqual(generated_slug, self.expected_slug)

    def test_title(self):
        generated_title = self.page_type._generate_title(self.data)
        self.assertEqual(generated_title, self.expected_title)

    def test_validation(self):
        """Tests the find_errors() method on the base class, including the
        custom validators."""
        initial_data = {
            'term': 'winter',
            'year': '2014',
            'content': 'test',
        }

        for invalid_data in self.invalid_inputs:
            # Basically incorporate all the possible context values
            data = {}
            data.update(initial_data)
            data.update(self.data)
            data.update(invalid_data)

            errors = self.page_type.find_errors(data)
            self.assertEqual(len(errors), 1)

        # Make sure the regular self.data dict doesn't trigger errors
        default_data = {}
        default_data.update(initial_data)
        default_data.update(self.data)
        self.assertFalse(self.page_type.find_errors(default_data))


class TestLectureNotes(_TestPageType):
    short_name = 'lecture-notes'
    data = {
        'date_weekday': 'tuesday',
        'date_month': 'april',
        'date_date': '15',
        'year': '2014',
    }
    expected_slug = 'tuesday-april-15'
    expected_title = 'Tuesday, April 15, 2014'
    invalid_inputs = [
        {
            'date_weekday': 'saturday',
        },
        {
            'date_month': 'not a month',
        },
        {
            'date_date': 'lol',
        },
        {
            'date_date': '0',
        },
        {
            'date_weekday': 'monday',  # it's actually a tuesday
            'date_month': 'april',
            'date_date': '15',
            'date_year': '2014',
        },
    ]


class TestPastExam(_TestPageType):
    short_name = 'past-exam'
    data = {
        'term': 'winter',
        'year': '2014',
        'exam_type': 'final',
    }
    expected_slug = 'final'
    expected_title = 'Winter 2014 Final'
    invalid_inputs = [{
        'exam_type': 'not a type',
    }]


class TestCourseSummary(_TestPageType):
    short_name = 'summary'
    data = {
        'subject': 'HTSEFP',
    }
    expected_slug = 'htsefp'
    expected_title = None
    invalid_inputs = [{
        'subject': '',
    }]


class TestVocabList(_TestPageType):
    short_name = 'vocab-list'
    data = {
        'subject': 'Vocabulary list',
    }
    expected_slug = 'vocabulary-list'
    expected_title = None
    invalid_inputs = [{
        'subject': '',
    }]


class TestCourseQuiz(_TestPageType):
    short_name = 'course-quiz'
    data = {
        'subject': 'Course quiz',
    }
    expected_slug = 'course-quiz'
    expected_title = None
    invalid_inputs = [{
        'subject': '',
    }]
