from django.db import models

class Course(models.Model):
	class Meta:
		app_label = 'wiki'

	department = models.ForeignKey('Department')
	number = models.IntegerField()
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255) # change this later
	credits = models.IntegerField()

	def __unicode__(self):
		return "%s %d (%s)" % (self.department.short_name, self.number, self.name)

	def url(self):
		return '/%s_%d' % (self.department.short_name, self.number)
