from django.test import TestCase
from wiki.models.courses import CourseSemester, Course
from wiki.models.faculties import Faculty
from wiki.models.departments import Department
from wiki.models.page_types import CourseQuiz
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

class PageTypesTest(TestCase):
	def test_course_quiz(self):
		self.maxDiff = None
		content = [
			'Heading\n',
			'---------\n',
			'* Question\n',
			'- Wrong\n',
			'+ Right\n',
			'- Wrong\n',
			'? Answer and explanation etc\n',
			'\n',
			'* Question2\n',
			'+ Right\n',
			'- Wrong\n',
			'- Wrong2\n',
			'? Answer 2\n',
		]
		data = {
			'questions': [
				{'number':1, 'heading': 'Heading\n---------', 'question': 'Question', 'choices': [{'number':0, 'text':'Wrong'}, {'number':1, 'text':'Right'}, {'number':2, 'text':'Wrong'}], 'correct': 1, 'answer': 'Answer and explanation etc'},
				{'number':2, 'heading': '', 'question': 'Question2', 'choices': [{'number':0, 'text':'Right'}, {'number':1, 'text':'Wrong'}, {'number':2, 'text':'Wrong2'}], 'correct': 0, 'answer': 'Answer 2'}, 
			],
		}
		obj = CourseQuiz()
		self.assertEqual(data, obj.format(content))

	def test_save_course_quiz(self):
		obj = CourseQuiz()
		
