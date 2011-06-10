from django.db import models
from semesters import Semester
from courses import Course

# The "base" page class - all specific page types have a one-to-one relationship with this
class Page(models.Model):
	course = Model.ForeignKey(Course)
	# Determines how many files are needed. Always user-configurable, even for vocab quizzes
	num_sections = Model.IntegerField()

# Oh fuck this is so awesome
class LectureNote(Page):
	num_sections = Model.IntegerField()
	semester = Model.ForeignKey(Semester)
	
class PastExam(Page):
	num_sections = Model.IntegerField()
	# Doesn't have a semester
	semester = None
	# The exam semester ... which means the oldest_year must be pushed back
	exam_semester = Model.ForeignKey(Semester)

class CourseQuiz(Page):
	semester = Model.ForeignKey(Semester)

class VocabQuiz(Page):
	semester = Model.ForeignKey(Semester)

# Includes miscellaneous shit too
class CourseSummary(Page):
	num_sections = Model.IntegerField()
	semester = Model.ForeignKey(Semester)
