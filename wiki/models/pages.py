from django.db import models
import utils

class Page(models.Model):
	class Meta:
		app_label = 'wiki'
		unique_together = ('course_sem', 'slug')

	course_sem = models.ForeignKey('CourseSemester')
	num_sections = models.IntegerField() # is this really necessary? sort of cache maybe?
	subject = models.CharField(max_length=255, null=True) # only used for some (most) page types
	link = models.CharField(max_length=255, null=True) # remember the max length. only used for some page_types
	page_type = models.CharField(choices=utils.page_type_choices, max_length=20)
	title = models.CharField(max_length=255, null=True) # the format of this is determined by the page type
	professor = models.ForeignKey('Professor', null=True)
	slug = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.get_title()

	def get_filepath(self):
		return "wiki/content%s/" % self.get_url() # looks rather silly but it actually does work!

	def get_title(self):
		type_name = utils.page_types[self.page_type].long_name # lol
		if not self.title:
			return "%s - %s (%s %s)" % (type_name, self.subject, self.course_sem.term.title(), self.course_sem.year)
		else:
			return "%s - %s" % (type_name, self.title)

	def get_url(self):
		course = self.course_sem.course
		page_type_obj = utils.page_types[self.page_type]
		return "%s/%s/%s-%s/%s" % (course.url(), self.page_type, self.course_sem.term, self.course_sem.year, self.slug)

	def load_sections(self, page_type_obj):
		path = self.get_filepath()
		sections = []
		for i in xrange(1, self.num_sections + 1):
			filename = "%s%d.md" % (path, i)
			file = open(filename, 'r')
			file_lines = file.readlines()
			title = file_lines[0][:-1] # strip the newline char
			content = file_lines[3:]
			section = Section(title, content, i)
			section.format(page_type_obj)
			sections.append(section)

		return sections

	def save_sections(self, data, username, email):
		path = self.get_filepath()
		num_sections = int(data['num_sections'])
		repo = utils.Git(path) # Will take care of making the directories
		for i in xrange(1, num_sections + 1):
			filename = "%s%d.md" % (path, i)
			file = open(filename, 'wb')
			title = data["section-%d-title" % i]
			body = data["section-%d-body" % i]
			body = body.replace('^M', '\n')
			file.write(title + '\n')
			file.write('--------\n\n')
			file.write(body + '\n') # necessary for some reason
			file.close()
			repo.add("%d.md" % i)
		repo.commit(data['message'], username, email)

# Not actually a model, more of a helper class to manage sections more easily
class Section:
	def __init__(self, title, content, number):
		self.title = title
		self.content = content
		self.number = number
		self.body = "\n".join(content) # For editing etc

	def format(self, page_type_obj):
		self.data = page_type_obj.format(self.content) # needs a better naming scheme
