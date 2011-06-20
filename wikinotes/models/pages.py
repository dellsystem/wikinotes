from django.db import models
from wikinotes.models.courses import CourseSemester
from wikinotes.utils.pages import get_possible_exams, get_weekday_dates
from wikinotes.utils.semesters import get_possible_semesters

class WeekdayDateField(models.Field):
	description = 'For dates like Monday April 25 blah. No year, only weekdays'
	def __init__(self, *args, **kwargs):
		current_semester = args[0]
		kwargs['max_length'] = 30 # idk
		# kwargs['choices'] = get_weekday_dates()
		super(WeekdayDateField, self).__init__(*args, **kwargs)
	def get_internal_type(self):
		return 'CharField'

def get_to_str_choices():
	return (
		('semester subject', '[Semester] [Subject]'),
		('subject (semester)', '[Subject] ([Semester])'),
		('date (semester)', '[Date] ([Semester])'),
	)

# Convert a semester like Winter 2001 into something slug-friendly like winter-2001
def to_slug(semester):
	semester = semester.lower()
	semester = semester.replace(' ', '-')
	# Remove commas, too
	semester = semester.replace(',', '')
	return semester

# To allow more customisation eventually
class PageType(models.Model):
	class Meta:
		app_label = 'wikinotes'
	
	# If the date is needed, then the slug will use the date
	need_date = models.BooleanField(verbose_name="Uses the date field")
	name = models.CharField(max_length=30)
	# e.g. "lecture" "exam" "vocabquiz"
	slug = models.SlugField(unique=True)
	to_str = models.CharField(max_length=20, choices=get_to_str_choices(), verbose_name="String representation")
	
	def __unicode__(self):
		return self.name
	
	"""
		Exam - [Semester] [Subject]
		Lecture notes - [Weekday Date] (Winter 2011)
		Multiple choice quiz - [Subject] (Winter 2011)
		Vocabulary quiz - [Subject] (Winter 2011)
		Summary - [Subject] (Winter 2011)
		
		/summary/winter-2011/blah-blah/
		/exam/winter-2011/final/
		/quiz/winter-2011/blah-blah/
		/vocab/winter-2011/blah-blah/
		/lecture/winter-2011/monday-april-23/
		
		or maybe /MATH_150/winter-2011/lecture/monday-april-23/
	"""

# The "base" page class - all specific page types have a one-to-one relationship with this
class Page(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	course_semester = models.ForeignKey(CourseSemester)
	# Determines how many files are needed. Always user-configurable, even for vocab quizzes
	num_sections = models.IntegerField()
	page_type = models.ForeignKey(PageType)
	
	# For past exams, the choices are Midterm and Final
	subject = models.CharField(max_length=100)
	
	def _get_semester(self):
		return self.course_semester.semester
	
	semester = property(_get_semester)
	
	# Only needed for lecture notes
	date = WeekdayDateField(semester, blank=True)
	
	# Optional - in case there's a link to a reference document somewhere
	# For example, the original exam on the library website, or on docuum
	ref_link = models.URLField(blank=True, verify_exists=True)
	slug = models.SlugField(max_length=40)
	
	def __unicode__(self):
		prefix  = '%s -' % self.page_type
		if self.page_type.to_str == 'date (semester)' and self.page_type.need_date:
			long_name = '%s %s (%s)' % (prefix, self.date, self.course_semester.semester)
		elif self.page_type.to_str == 'semester subject':
			long_name = '%s %s %s' % (prefix, self.course_semester.semester, self.subject)
		else: # Assume page_type.to_str == 'subject (semester)'
			long_name = '%s %s (%s)' % (prefix, self.subject, self.course_semester.semester)
		return long_name
	
	def get_slug(self):
		# If need_date is defined as true, it will use the date as the slug; otherwise, subject
		slug_end = self.date if self.page_type.need_date else self.subject
		slug = '/%s/%s/%s' % (to_slug(self.course_semester.semester), self.page_type.slug, to_slug(slug_end))
		return (to_slug(slug_end), slug)
