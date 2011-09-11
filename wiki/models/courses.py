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

	def num_watchers(self):
		return 0

	def num_pages(self):
		return 0

class CourseSemester(models.Model):
	class Meta:
		app_label = 'wiki'

	course = models.ForeignKey('Course')
	grading_scheme = models.CharField(max_length=255)
	professors = models.ManyToManyField('Professor')
	schedule = models.CharField(max_length=100)
	midterm_info = models.CharField(max_length=255)
	final_info = models.CharField(max_length=255)

class Professor(models.Model):
	class Meta:
		app_label = 'wiki'

	name = models.CharField(max_length=100)
