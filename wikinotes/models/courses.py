from django.db import models
from wikinotes.models.departments import Department
from wikinotes.utils.semesters import get_possible_terms, get_possible_years
from wikinotes.models.professors import Professor

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
	term = models.CharField(max_length=6, choices=get_possible_terms())
	# Starting from 2009 for now, maybe make that configurable later
	year = models.IntegerField(max_length=4, choices=get_possible_years(2009))
	professors = models.ManyToManyField(Professor)
	
	# So like B+ A- etc
	course_avg = models.CharField(max_length=2)
