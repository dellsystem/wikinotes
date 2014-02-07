from django.test.client import Client
from django.test import TestCase

from wiki.models.faculties import Faculty


class _ViewTest(TestCase):
    fixtures = ['test']

    def setUp(self):
        client = Client()
        self.response = client.get(self.url)

    def test_title(self):
        title = self.response.context['title']
        self.assertEqual(title, self.title)

    def test_first_template(self):
        self.assertEqual(self.response.templates[0].name, self.template)


# class RemoveSlashTest:


class FacultyOverviewTest(_ViewTest):
    url = '/faculty/science/'
    title = 'Faculty of Science'
    template = 'courses/faculty_overview.html'

    def test_context(self):
        context = self.response.context

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
