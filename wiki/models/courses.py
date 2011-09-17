from django.db import models

class Course(models.Model):
	class Meta:
		app_label = 'wiki'

	department = models.ForeignKey('Department')
	number = models.IntegerField()
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255) # change this later
	credits = models.IntegerField() # Note - what if it's a float etc

	def __unicode__(self):
		return "%s %d" % (self.department.short_name, self.number)

	def url(self):
		return '/%s_%d' % (self.department.short_name, self.number)

	def num_watchers(self):
		return 0

	def num_pages(self):
		return 0

class CourseSemester(models.Model):
	class Meta:
		app_label = 'wiki'
		unique_together = ('term', 'year')

	course = models.ForeignKey('Course')
	grading_scheme = models.CharField(max_length=255, null=True)
	professors = models.ManyToManyField('Professor', null=True)
	schedule = models.CharField(max_length=100, null=True)
	midterm_info = models.CharField(max_length=255, null=True)
	final_info = models.CharField(max_length=255, null=True)
	term = models.CharField(max_length=6) # Winter/Summer etc
	year = models.CharField(max_length=4) # Because ... yeah

	def __unicode__(self):
		return "%s (%s %s)" % (self.course, self.term, self.year)

class Professor(models.Model):
	class Meta:
		app_label = 'wiki'

	name = models.CharField(max_length=100)
