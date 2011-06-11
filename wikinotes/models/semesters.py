from django.db import models
from wikinotes.utils.semesters import get_possible_years, get_possible_terms
from wikinotes.models.courses import Course

# Kind of like an enum in java lol
class Semester(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	# Can be Summer, Spring or Winter
	term = models.CharField(max_length=6, choices=get_possible_terms())
	year = models.IntegerField(max_length=4, choices=get_possible_years())
	
	def __unicode__(self):
		return "%s (%d)" % (self.term, self.year)

# Includes the name of the prof. Each page should be tied to a semester I think
class CourseSemester(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	course = models.ForeignKey(Course)
	semester = models.ForeignKey(Semester)
	
	# Text field for now maybe ManyToMany later ugh
	prof = models.CharField(max_length=50)
	# So like B+ A- etc
	course_avg = models.CharField(max_length=2)
	
	def get_prof(self):
		return self.prof
