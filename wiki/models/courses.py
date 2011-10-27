from django.db import models
from django.contrib.auth.models import User
from wiki.models.history import HistoryItem

class Course(models.Model):
	class Meta:
		app_label = 'wiki'

	department = models.ForeignKey('Department')
	number = models.IntegerField()
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255) # change this later
	credits = models.IntegerField() # Note - what if it's a float etc
	watchers = models.ManyToManyField(User)
	# The latest_activity field makes it easier to sort and stuff ... not strictly necessary
	latest_activity = models.ForeignKey('HistoryItem', related_name='latest_course', null=True) # stupid but won't validate without it
	num_watchers = models.IntegerField(default=0) # caches it basically

	def __unicode__(self):
		return "%s %d" % (self.department.short_name, self.number)

	def get_url(self):
		return '/%s_%d' % (self.department.short_name, self.number)

	def num_pages(self):
		count = 0
		course_sems = self.coursesemester_set.all()
		for sem in course_sems:
			num_pages = sem.page_set.count()
			count += num_pages
		return count

	# Use this for adding an event to a course
	def add_event(self, user=None, action=None, page=None, message=''):
		new_item = HistoryItem(user=user, action=action, page=page, message=message, course=self)
		new_item.save()
		self.latest_activity = new_item
		self.save()

	# Get history items for this course; limited to 5 when called from the template
	# Set to 0 for no limit
	def recent_activity(self, limit=5):
		course_history = HistoryItem.objects.filter(course=self)
		if limit > 0:
			return course_history[:limit]
		else:
			return course_history

class CourseSemester(models.Model):
	class Meta:
		app_label = 'wiki'
		unique_together = ('term', 'year', 'course')

	course = models.ForeignKey('Course')
	grading_scheme = models.CharField(max_length=255, null=True)
	professors = models.ManyToManyField('Professor', null=True)
	schedule = models.CharField(max_length=100, null=True)
	midterm_info = models.CharField(max_length=255, null=True)
	final_info = models.CharField(max_length=255, null=True)
	term = models.CharField(max_length=6) # Winter/Summer etc
	year = models.IntegerField(max_length=4) # Because ... yeah

	def __unicode__(self):
		return "%s (%s %d)" % (self.course, self.term.title(), self.year)

	def get_semester(self):
		# For printing out. Returns Term year
		return "%s %d" % (self.term.title(), self.year)

class Professor(models.Model):
	class Meta:
		app_label = 'wiki'

	name = models.CharField(max_length=100)
