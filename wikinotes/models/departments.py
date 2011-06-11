from django.db import models
from wikinotes.models.faculties import Faculty

class Department(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	# Use the short name as the primary key. It makes sense.
	name = models.CharField(max_length=4, primary_key=True)
	long_name = models.CharField(max_length=255)
	faculty = models.ForeignKey(Faculty)
	
	# The short name (e.g. MATH) should be shown as a representation
	def __unicode__(self):
		return self.name
	
	# Returns the long name (e.g. Mathematics & Statistics)
	def get_long_name(self):
		return self.long_name
