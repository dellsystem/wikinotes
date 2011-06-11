from django.db import models
from wikinotes.models.courses import Course

class Blah(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	course = models.ManyToManyField(Course)
