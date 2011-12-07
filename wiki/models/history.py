from django.db import models
from django.contrib.auth.models import User
from wiki.utils.history import get_date_x_days_ago, humanise_timesince

class HistoryManager(models.Manager):
	# Returns all the HistoryItems with a timestamp between now and x days ago
	def get_since_x_days(self, num_days, show_all):
		# If show_all is False, ignore watch actions (that's all it means)
		cutoff_date = get_date_x_days_ago(int(num_days))
		query_set = self.filter(timestamp__gt=cutoff_date).order_by('-timestamp')
		if not show_all:
			query_set = query_set.exclude(page__isnull=True)
		return query_set


class HistoryItem(models.Model):
	class Meta:
		app_label = 'wiki'

	objects = HistoryManager()
	user = models.ForeignKey(User)
	action = models.CharField(max_length=30)
	timestamp = models.DateTimeField(auto_now=True)
	page = models.ForeignKey('Page', null=True)
	message = models.CharField(max_length=255, null=True)
	course = models.ForeignKey('Course')
	#sha = models.CharField(max_length=40, null=True) # only used for page editing/creation

	def __unicode__(self):
		return 'timestamp: %s, course: %s' % (self.timestamp, self.course)

	def get_timesince(self):
		return humanise_timesince(self.timestamp)

# You can create a page, and you can edit a page ... good enough for now
