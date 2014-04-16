# NOT ACTUALLY DJANGO MODELS
# Done this way because it's better than the 4 other possible ways (believe me I tried them all)
# Define all the page types here, and their short names
import re

from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from wiki.utils.constants import terms, years, exam_types


class PageType:
    # Defaults - override if necessary
    uneditable_fields = ['semester', 'subject']
    editable_fields = ['professor_id', 'link']
    metadata_fields = ['professor', 'link']
    has_subject = True

    def _generate_slug(self, data):
        """Override this method to change the way the slug is generated."""
        return slugify(data['subject'])

    def _generate_title(self, data):
        """Override this method if a title needs to be set. Otherwise, if a
        title is not set, WikiNotes will default to using the name of the page
        type and the subject."""
        return None

    def get_kwargs(self, data):
        """Do not override. To change the way slugs or titles are generated, see
        the previous two methods."""
        kwargs = {
            'link': data['link'],
            'professor_id': data['professor_id'],
            'slug': self._generate_slug(data),
            'title': self._generate_title(data),
        }

        if self.has_subject:
            kwargs['subject'] = data['subject']

        return kwargs

    # Some of these are unused, clean them up sometime
    def get_cell_template(self):
        return 'pages/%s/cell.html' % self.short_name

    def get_metadata_template(self):
        return 'pages/%s/metadata.html' % self.short_name

    # Wrapper around short_name basically
    def get_form_template(self):
        return 'pages/%s/create_form.html' % self.short_name

    def get_help_template(self):
        return 'pages/%s/create_help.html' % self.short_name

    # For showing ONE page of this type
    def get_show_template(self):
        return 'pages/%s/show.html' % self.short_name

    # For showing all the pages of this type (on a per-course level)
    def get_list_template(self):
        return 'pages/%s/list' % self.short_name

    def get_list_header(self):
        return self.get_list_template() + '_header.html'

    def get_list_body(self):
        return self.get_list_template() + '_body.html'

    def get_icon(self):
        return '/static/img/pages/%s.png' % self.short_name

    def get_url_args(self, course):
        url_args = course.get_url_args()
        return url_args + (self.short_name,)

    def get_url(self, course):
        return reverse('courses_category_overview',
            args=self.get_url_args(course))

    def get_create_url(self, course):
        return reverse('pages_create', args=self.get_url_args(course))

    @staticmethod
    def get_field_templates(fields):
        return ['pages/%s_field.html' % field for field in fields]

    def get_editable_fields(self):
        return self.get_field_templates(self.editable_fields)

    def get_uneditable_fields(self):
        return self.get_field_templates(self.uneditable_fields)

    def find_errors(self, data):
        validators = self.get_validators(data) + [
            (data['term'] in terms, 'Invalid term'),
            (int(data['year']) in years, 'Invalid year'),
            (len(data['content'].strip()) > 0, 'No content'),
        ]

        errors = []

        for validator in validators:
            if not validator[0]:
                errors.append(validator[1])

        return errors


class LectureNote(PageType):
    short_name = 'lecture-notes'
    long_name = 'Lecture notes'
    description = 'Notes from a lecture given by a specific professor on a specific date'
    uneditable_fields = ['semester', 'date']
    # Subject IS editable in this case only because it's not part of the slug
    editable_fields = ['subject', 'professor_id', 'link']
    metadata_fields = ['subject', 'professor', 'link']

    def _generate_title(self, data):
        weekday = data['date_weekday']
        month = data['date_month']
        date = data['date_date']
        year = data['year']
        return "%s, %s %s, %s" % (weekday.title(), month.title(), date, year)

    def _generate_slug(self, data):
        weekday = data['date_weekday']
        month = data['date_month']
        date = data['date_date']
        year = data['year']
        return "%s-%s-%s" % (weekday, month, date)

    def get_validators(self, data):
        return []


class PastExam(PageType):
    short_name = 'past-exam'
    long_name = 'Past exam'
    description = 'Student-made solutions to a past exam'
    uneditable_fields = ['semester', 'exam']
    has_subject = False

    def _generate_slug(self, data):
        return data['exam_type']

    def _generate_title(self, data):
        term = data['term']
        year = data['year']
        exam_type = data['exam_type']
        return "%s %s %s" % (term.title(), year, exam_type.title())

    def get_validators(self, data):
        return [
            (data['exam_type'] in exam_types, 'Invalid exam type'),
        ]


class CourseSummary(PageType):
    short_name = 'summary'
    long_name = 'Course summary'
    description = 'Anything that doesn\'t fit in the other categories'

    def get_validators(self, data):
        return [
            (len(data['subject']) > 0, 'Invalid subject'),
        ]


class VocabList(PageType):
    short_name = 'vocab-list'
    long_name = 'Vocabulary list'
    description = 'For memorising terms etc'

    def get_validators(self, data):
        return [
            (len(data['subject']) > 0, 'Invalid subject'),
        ]


class CourseQuiz(PageType):
    short_name = 'course-quiz'
    long_name = 'Multiple choice quiz'
    description = 'A quiz for testing your knowledge'

    def get_validators(self, data):
        return [
            (len(data['subject']) > 0, 'Invalid subject'),
        ]
