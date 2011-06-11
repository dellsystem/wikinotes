from django.db import models
from wikinotes.models.departments import Department

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
