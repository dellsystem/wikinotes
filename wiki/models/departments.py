from django.db import models

class Department(models.Model):
	class Meta:
		app_label = 'wiki'

	short_name = models.CharField(max_length=4, primary_key=True)
	long_name = models.CharField(max_length=255)
	faculty = models.ForeignKey('Faculty')

	def __unicode__(self):
		return "%s (%s)" % (self.short_name, self.long_name)
