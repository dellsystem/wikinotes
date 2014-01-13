from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

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
    hexsha = models.CharField(max_length=40, null=True) # only used for page editing

    def __unicode__(self):
        return 'timestamp: %s, course: %s' % (self.timestamp, self.course)

    def get_timesince(self):
        return humanise_timesince(self.timestamp)

    def get_absolute_url(self):
        if self.page:
            if self.hexsha:
                url_args = self.page.get_url_args() + (self.hexsha,)
                return reverse('pages_commit', args=url_args)
            else:
                return self.page.get_history_url()
        else:
            return self.course.get_recent_url()

    def get_short_hexsha(self):
        if self.hexsha:
            return self.hexsha[:7]
        else:
            return ''
