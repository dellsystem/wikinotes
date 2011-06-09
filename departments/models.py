from django.db import models

class Department(models.Model):
	name = models.CharField(max_length=4)
	long_name = models.CharField(max_length=255)
	
	# The short name (e.g. MATH) should be shown as a representation
	def __unicode__(self):
		return self.name
