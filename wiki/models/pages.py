from django.db import models
import utils

class Page(models.Model):
	class Meta:
		app_label = 'wiki'

	course_sem = models.ForeignKey('CourseSemester')
	num_sections = models.IntegerField() # is this really necessary? sort of cache maybe?
	subject = models.CharField(max_length=255, null=True) # only used for some (most) page types
	link = models.CharField(max_length=255, null=True) # remember the max length. only used for some page_types
	page_type = models.CharField(choices=utils.page_type_choices, max_length=20)
	title = models.CharField(max_length=255, null=True) # the format of this is determined by the page type
	professor = models.ForeignKey('Professor', null=True)

	# Calls the relevant model defined on the specified page type
	def is_subject_valid(self):
		real_type = utils.page_types[self.page_type]
		return real_type.is_subject_valid(self.subject)

	def __unicode__(self):
		return self.get_title()

	def get_title(self):
		type_name = utils.page_types[self.page_type].long_name # lol
		if not self.title:
			return "%s - %s (%s %s)" % (type_name, self.subject, self.course_sem.term, self.course_sem.year)
		else:
			return "%s - %s" % (type_name, self.title)

	def get_url(self):
		course = self.course_sem.course
		page_type_obj = utils.page_types[self.page_type]
		return "%s/%s/%s-%s/%s" % (course.url(), self.page_type, self.course_sem.term, self.course_sem.year, page_type_obj.get_slug(self))
