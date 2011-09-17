from django.test import TestCase
from wiki.models.courses import CourseSemester, Course
from wiki.models.faculties import Faculty
from wiki.models.departments import Department
from django.db import IntegrityError

class CourseSemesterTest(TestCase):
	def setUp(self):
		faculty = Faculty(name='Faculty of Science', slug='science')
		faculty.save()
		department = Department(short_name='BIOL', faculty=faculty, long_name='Biology')
		department.save()
		self.course = Course(department=department, number=112, description="lol", credits=3)
		self.course.save()
		self.course_sem_1 = CourseSemester(term='Winter', year='2011', course=self.course)
		self.course_sem_1.save()
		self.course_sem_2 = CourseSemester(term='Summer', year='2011', course=self.course)
		self.course_sem_2.save()

	def test_same_semester(self):
		duplicate = CourseSemester(term='Winter', year='2011', course=self.course)
		self.assertRaises(IntegrityError, duplicate.save)

	def test_get_semester(self):
		course_sem_1 = CourseSemester.objects.get(term='Winter', year='2011', course=self.course)
		self.assertEqual(course_sem_1, self.course_sem_1)
		self.assertRaises(CourseSemester.DoesNotExist, CourseSemester.objects.get, term='Summer', year='1999', course=self.course)
