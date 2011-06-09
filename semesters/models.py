from django.db import models
from utils import get_possible_years, get_possible_terms
from courses.models import Course

# Kind of like an enum in java lol
class Semester(models.Model):
	# Can be Summer, Spring or Winter
	term = models.CharField(max_length=6, choices=get_possible_terms())
	year = models.IntegerField(max_length=4, choices=get_possible_years())
	
	def __unicode__(self):
		return "%s (%d)" % (self.term, self.year)

# Includes the name of the prof. Each page should be tied to a semester I think
class CourseSemester(models.Model):
	course = models.ForeignKey(Course)
	semester = models.ForeignKey(Semester)
	# Text field for now maybe ManyToMany later ugh
	prof = models.CharField(max_length=50)
