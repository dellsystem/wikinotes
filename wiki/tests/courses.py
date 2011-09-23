from django.test import TestCase
from wiki.models.courses import CourseSemester, Course

class CourseSemesterTest(TestCase):
	def test_same_semester(self):
		course = Course.objects.get(pk=1)
		course_sem_1 = CourseSemester(term='Winter', year='2011', course=course)
		course_sem_1.save()
		course_sem_2 = CourseSemester(term='Summer', year='2011', course=course)
		course_sem_2.save()
		course_sem_3 = CourseSemester(term='Winter', year='2011', course=course)
		course_sem_3.save()
		print "lol"
