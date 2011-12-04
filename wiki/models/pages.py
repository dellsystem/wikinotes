from django.db import models
from wiki.utils.pages import page_types, page_type_choices#, get_page_type
from wiki.utils.gitutils import Git
import os
from wiki.models.courses import CourseSemester

class Page(models.Model):
	class Meta:
		app_label = 'wiki'
		unique_together = ('course_sem', 'slug')

	course_sem = models.ForeignKey('CourseSemester')
	subject = models.CharField(max_length=255, null=True) # only used for some (most) page types
	link = models.CharField(max_length=255, null=True) # remember the max length. only used for some page_types
	page_type = models.CharField(choices=page_type_choices, max_length=20)
	title = models.CharField(max_length=255, null=True) # the format of this is determined by the page type
	professor = models.ForeignKey('Professor', null=True)
	slug = models.CharField(max_length=50)

	def load_content(self):
		file = open('%scontent.md' % self.get_filepath())
		content = file.read()
		file.close()
		return content

	def edit(self, data):
		page_type = page_types[self.page_type]
		# Change the relevant attributes
		for editable_field in page_type.editable_fields:
			if editable_field != 'professor':
				setattr(self, editable_field, data[editable_field])
		self.save()
		# THE FOLDER SHOULD NOT HAVE TO BE MOVED!!! NOTHING IMPORTANT NEEDS TO BE CHANGED!!!

	def save_content(self, content, message, username):
		path = self.get_filepath()
		repo = Git(path)
		filename = '%scontent.md' % path
		file = open(filename, 'wt')
		file.write(content)
		file.close()
		repo.add('content.md')
		message = 'Minor edit' if not message else message
		repo.commit(message, username, 'example@example.com')

	def __unicode__(self):
		return self.get_title()

	def get_filepath(self):
		return "wiki/content%s/" % self.get_url()

	def get_type(self):
		return page_types[self.page_type]
	
	def get_title(self):
		if not self.subject:
			return self.title
		else:
			return self.subject

	def get_url(self):
		course = self.course_sem.course
		return "%s/%s/%s-%s/%s" % (course.get_url(), self.page_type, self.course_sem.term, self.course_sem.year, self.slug)
