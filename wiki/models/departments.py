from django.core.urlresolvers import reverse
from django.db import models


class Department(models.Model):
    short_name = models.CharField(max_length=4, primary_key=True)
    long_name = models.CharField(max_length=255)
    faculty = models.ForeignKey('Faculty')
    url_fields = {
        'department': 'short_name__iexact',
    }

    class Meta:
        app_label = 'wiki'
        ordering = ['short_name']

    def __unicode__(self):
        return "Department of %s (%s)" % (self.long_name, self.short_name)

    def get_absolute_url(self):
        return reverse('courses_department_overview', args=[self.pk])

    def get_image(self):
        return "/static/img/department/%s.png" % self.short_name

    def get_large_image(self):
        return "/static/img%s_large.png" % self.get_absolute_url()
