from django.db import models

class Department(models.Model):
	# Use the short name as the primary key. It makes sense.
	name = models.CharField(max_length=4, primary_key=True)
	long_name = models.CharField(max_length=255)
	
	# The short name (e.g. MATH) should be shown as a representation
	def __unicode__(self):
		return self.name
	
	# Returns the long name (e.g. Mathematics & Statistics)
	def get_long_name(self):
		return self.long_name
