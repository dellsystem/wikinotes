from django.db import models

class Professor(models.Model):
	class Meta:
		app_label = 'wikinotes'

	name = models.CharField(max_length=100)
	# Might need a department later, but what if profs can teach in more than one?
	
	def __unicode__(self):
		return self.name
