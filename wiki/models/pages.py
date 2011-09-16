from django.db import models
import utils

class Page(models.Model):
	class Meta:
		app_label = 'wiki'

	course_semester = models.ForeignKey('CourseSemester')
	num_sections = models.IntegerField() # is this really necessary? sort of cache maybe?
	subject = models.CharField(max_length=255)
	link = models.CharField(max_length=255) # source of a bug later on? lol
	page_type = models.CharField(choices=utils.page_type_choices, max_length=20)

	# Calls the relevant model defined on the specified page type
	def is_subject_valid(self):
		real_type = utils.page_types[self.page_type]
		return real_type.is_subject_valid(self.subject)
