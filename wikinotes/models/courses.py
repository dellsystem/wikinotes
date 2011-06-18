from django.db import models
from wikinotes.models.departments import Department
from wikinotes.utils.semesters import get_possible_terms, get_possible_years, get_possible_semesters
from wikinotes.models.professors import Professor

class SemesterField(models.Field):
	description = 'A semester in the format [Term] [Year]'
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 7 # That is the length of 'Winter 2011' and is the longest possible
		kwargs['choices'] = get_possible_semesters()
		super(SemesterField, self).__init__(*args, **kwargs)
	def get_internal_type(self):
		return 'CharField'
	def get_year(self):
		# Just return the last four digits
		return str(self)[-4:]

class Course(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	department = models.ForeignKey(Department)
	number = models.IntegerField()
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	credits = models.IntegerField()
	
	# The department + number should be shown
	def __unicode__(self):
		return "%s %d" % (self.department, self.number)
	
	def get_name(self):
		return self.name
	
	def get_description(self):
		return self.description
	
	def get_credits(self):
		return self.credits

class CourseSemester(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	course = models.ForeignKey(Course)
	semester = SemesterField()
	professors = models.ManyToManyField(Professor)
	
	# So like B+ A- etc. Should be optional
	course_avg = models.CharField(max_length=2, blank=True)
	def __unicode__(self):
		return "%s, %s" % (self.course, self.semester)
