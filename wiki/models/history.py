from django.db import models
from django.contrib.auth.models import User

class HistoryItem(models.Model):
	class Meta:
		app_label = 'wiki'

	user = models.ForeignKey(User)
	action = models.CharField(max_length=30)
	timestamp = models.DateTimeField(auto_now=True)
	page = models.ForeignKey('Page', null=True)
	message = models.CharField(max_length=255, null=True)
	course = models.ForeignKey('Course')

# You can create a page, and you can edit a page ... good enough for now
