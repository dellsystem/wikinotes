from django.db import models
from courses.models import Course

class User(models.Model):
	username = models.CharField(max_length=20)
	email = models.CharField(max_length=100)
	courses = models.ManyToManyField(Course)

	# Return the username
	def __unicode__(self):
		return self.username
