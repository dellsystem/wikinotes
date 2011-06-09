from django.db import models
from departments.models import Department

class Course(models.Model):
	department = models.ForeignKey(Department)
	number = models.IntegerField()
	name = models.CharField(max_length=255)
	
	# The department + number should be shown
	def __unicode__(self):
		return "%s %d" % (self.department, self.number)
