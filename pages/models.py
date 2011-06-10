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
	semester = Model.ForeignKey(Semester)
	lecture_num = Model.IntegerField()
	subject = Model.CharField(max_length=100)
	date = Model.DateField()
	
	# Stuff that will need to be displayed for all pages etc
	def __unicode__(self):
		return "Lecture %d (%s)" % (self.lecture_num, self.subject)
	
class PastExam(Page):
	# Exam types: final, midterm and that's all for now lol
	exam_type = Model.CharField(choices=get_possible_exams())
	# Doesn't have an associated semester
	# See if it's possible to move semester = ForeignKey into Page and just override it here
	semester = None
	# The exam semester (when the exam was written etc) ... which means the oldest_year must be pushed back
	exam_semester = Model.ForeignKey(Semester)
	
	# Display as: Winter 2008 final exam or Fall 2009 midterm exam
	def __unicode__(self):
		return "%s %s exam" % (self.exam_semester, self.exam_type)

class CourseQuiz(Page):
	semester = Model.ForeignKey(Semester)
	subject = Model.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s (course quiz)" % self.subject

# The difference between course and vocab quizzes:
# For course quizzes, you have a question, and several MC answers (like my lab practice final)
# For vocab quizzes, you just match shit (like terms, definitions etc)
class VocabQuiz(Page):
	semester = Model.ForeignKey(Semester)
	subject = Model.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s (vocabulary quiz)" % self.subject

# Includes miscellaneous shit too
class CourseSummary(Page):
	semester = Model.ForeignKey(Semester)
	subject = Model.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s (course summary)" % self.subject
