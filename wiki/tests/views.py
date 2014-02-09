from datetime import datetime

from django.test.client import Client
from django.test import TestCase
from mock import MagicMock

from wiki.models.faculties import Faculty
from wiki.models.pages import Page
from wiki.utils import gitutils
from wiki.utils.tools import Struct


class _ViewTest(TestCase):
    fixtures = ['test']
    login_first = False

    def runTest(self):
        client = Client()
        if self.login_first:
            # Should get a redirect when attempting to send a GET request
            initial_response = client.get(self.url)
            self.assertEqual(initial_response.status_code, 302)

            client.post('/login/', {
                'username': 'user',
                'password': 'user',
                'login': 1,
            })

        response = client.get(self.url)

        # Make sure that the status is OK
        self.assertEqual(response.status_code, 200)

        # Check that the title is correct
        try:
            title = response.context['title']
        except KeyError:
            title = None
        self.assertEqual(title, self.title)

        # Check that the template file being used is correct
        self.assertEqual(response.templates[0].name, self.template)

        # Call the check_context function to perform any additional checks
        self.check_context(response.context)

    def check_context(self, context):
        """Override this method to do assertions on the returned context.
        """
        pass


"""
views/courses.py
"""


# class RemoveSlashTest:


class FacultyOverviewTest(_ViewTest):
    url = '/faculty/science/'
    title = 'Faculty of Science'
    template = 'courses/faculty_overview.html'

    def check_context(self, context):
        expected_faculty = Faculty.objects.get(slug='science')
        self.assertEqual(context['faculty'], expected_faculty)

        course_names = [str(course) for course in context['courses']]
        expected_course_names = ['BIOL 111', 'BIOL 112', 'MATH 150']
        self.assertEqual(course_names, expected_course_names)

        departments = [department.pk for department in context['departments']]
        expected_departments = ['BIOL', 'MATH']
        self.assertEqual(departments, expected_departments)


class DepartmentOverviewTest(_ViewTest):
    url = '/MATH/'
    title = 'Department of Mathematics & Statistics (MATH)'
    template = 'courses/department_overview.html'


class FacultyBrowseTest(_ViewTest):
    url = '/courses/faculty/'
    title = 'Browse by faculty'
    template = 'courses/faculty_browse.html'


class DepartmentBrowseTest(_ViewTest):
    url = '/courses/department/'
    title = 'Browse by department'
    template = 'courses/department_browse.html'


class ProfessorBrowseTest(_ViewTest):
    url = '/courses/professor/'
    title = 'Browse by professor'
    template = 'courses/professor_browse.html'


# class RandomCourseTest:


class CourseIndexTest(_ViewTest):
    url = '/courses/'
    title = 'Courses'
    template = 'courses/index.html'


class PopularBrowseTest(_ViewTest):
    url = '/courses/popular/'
    title = 'Browse courses by popularity'
    template = 'courses/all_browse.html'


class ActiveBrowseTest(_ViewTest):
    url = '/courses/active/'
    title = 'Browse courses by activity'
    template = 'courses/all_browse.html'


class AllBrowseTest(_ViewTest):
    url = '/courses/all/'
    title = 'Browse all courses'
    template = 'courses/all_browse.html'


# class WatchCourseTest:


# class GetAllTest:


class CourseOverviewTest(_ViewTest):
    url = '/MATH_150/'
    title = 'MATH 150'
    template = 'courses/overview.html'


class SemesterOverviewTest(_ViewTest):
    url = '/MATH_150/fall-2011/'
    title = 'MATH 150 (Fall 2011)'
    template = 'courses/semester_overview.html'


class CourseRecentActivityTest(_ViewTest):
    url = '/MATH_150/recent/'
    title = 'Recent activity for MATH 150'
    template = 'courses/recent.html'


class CategoryOverviewTest(_ViewTest):
    url = '/MATH_150/summary/'
    title = 'Course summary content for MATH 150'
    template = 'courses/category_overview.html'


class ProfessorOverviewTest(_ViewTest):
    url = '/professor/james-loveys/'
    title = 'Overview for James G Loveys'
    template = 'courses/professor_overview.html'


# class CourseCreateTest:


"""
views/main.py
"""


# class MainIndexTest:
# Not really sure how to test this one as it depends on logged-in status


# class LoginLogoutTest:


class RecentActivityTest(_ViewTest):
    url = '/recent/'
    title = 'Recent activity in the past 1 day(s)'
    template = 'main/recent.html'


# class RecentActivityAllTest:


# class RecentActivity30DaysTest:


# class ExploreTest:


class UserProfileTest(_ViewTest):
    url = '/users/user/'
    title = 'Viewing profile for user'
    template = 'main/profile.html'


class UserContributionsTest(_ViewTest):
    url = '/users/user/contributions/'
    title = 'Viewing contributions for user'
    template = 'main/contributions.html'


# class RegisterTest:


# class UcpTest:


# class MarkdownTest:


# class SearchTest


# class StaticTest


"""
views/pages.py
"""


class ShowPageTest(_ViewTest):
    url = '/MATH_150/summary/fall-2011/page-number-1/'
    title = 'Page number 1 - MATH 150 (Fall 2011)'
    template = 'pages/show.html'

    def check_context(self, context):
        page = context['page']
        self.assertEqual(page.content, '<p>lol</p>')


class PrintViewTest(_ViewTest):
    url = '/MATH_150/summary/fall-2011/page-number-1/print/'
    title = None  # set directly in the template
    template = 'pages/printview.html'

    def check_context(self, context):
        page = context['page']
        self.assertEqual(page.content, '<p>lol</p>')


class PageHistoryTest(_ViewTest):
    url = '/MATH_150/summary/fall-2011/page-number-1/history/'
    title = 'Page history for Page number 1 - MATH 150 (Fall 2011)'
    template = 'pages/history.html'

    def setUp(self):
        # Mock some methods on the Git class as the repo doesn't actually exist.
        gitutils.Git.__init__ = MagicMock(return_value=None)
        gitutils.Git.get_history = MagicMock(return_value=[{
            'get_date': datetime(2000, 1, 1),
            'author_name': 'user',
            'message': 'test',
            'num_lines': 0,
            'num_insertions': 0,
            'num_deletions': 0,
            'get_diff': [],
        }])

    def check_context(self, context):
        gitutils.Git.__init__.assert_called_with('wiki/content/MATH_150/'
            'summary/fall-2011/page-number-1/')
        history = context['commit_history']
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['message'], 'test')


class CommitViewTest(_ViewTest):
    url = ('/MATH_150/summary/fall-2011/page-number-1/commit/'
           '1234567890123456789012345678901234567890/')
    title = 'Commit information for Page number 1 - MATH 150 (Fall 2011)'
    template = 'pages/commit.html'

    def setUp(self):
        # Mock some methods in the gitutils module.
        gitutils.Git.get_commit = MagicMock(return_value=Struct({
            'get_date': datetime(2000, 1, 1),
            'author_name': 'user',
            'message': 'test',
            'num_lines': 0,
            'num_insertions': 0,
            'num_deletions': 0,
            'get_diff': [],
        }))

    def check_context(self, context):
        gitutils.Git.get_commit.assert_called_with('12345678901234567890'
            '12345678901234567890')
        commit = context['commit']
        self.assertEqual(commit.message, 'test')


# TODO: test the POST method, and merge conflicts
class EditPageTest(_ViewTest):
    url = '/MATH_150/summary/fall-2011/page-number-1/edit/'
    title = 'Editing Page number 1 - MATH 150 (Fall 2011)'
    template = 'pages/edit.html'
    login_first = True

    def setUp(self):
        gitutils.Git.get_latest_commit_hash = MagicMock(return_value='hash')
        Page.load_content = MagicMock(return_value='content')

    def check_context(self, context):
        self.assertTrue(context['latest_commit'], 'hash')
        self.assertTrue(context['content'], 'content')


# TODO: test for redirects
# class RandomPageTest:
