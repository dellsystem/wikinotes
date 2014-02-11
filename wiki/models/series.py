from django.db import models


class SeriesManager(models.Manager):
    """
    This custom manager is defined solely for the purpose of allowing hidden series
    """
    def visible(self, user, **kwargs):
        if user.is_staff:
            return self.filter(**kwargs)
        else:
            return self.filter(is_hidden=False, **kwargs)


class Series(models.Model):
    objects = SeriesManager()
    course = models.ForeignKey('Course')
    name = models.CharField(max_length=255)
    position = models.IntegerField()
    slug = models.SlugField()
    banner = models.ForeignKey('SeriesBanner', null=True, blank=True)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        app_label = 'wiki'
        unique_together = (('course', 'position'), ('course', 'slug'))
        verbose_name_plural = 'Series'

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.course)

    def get_absolute_url(self):
        """This can't use `reverse` because it includes an anchor link."""
        return self.course.get_absolute_url() + '#series-' + self.slug

    def can_view(self, user):
        return not self.is_hidden or user.is_staff

    def get_num_total(self):
        return self.seriespage_set.count()

    def get_next_position(self):
        query = self.seriespage_set.all().aggregate(models.Max('position'))
        max_position = query['position__max']
        if max_position:
            return max_position + 1
        else:
            return 1


class SeriesPage(models.Model):
    page = models.ForeignKey('Page')
    series = models.ForeignKey('Series')
    position = models.IntegerField('position')

    class Meta:
        app_label = 'wiki'
        # Each page can only be in a series once, each series can have only one page per position
        unique_together = (('position', 'series'), ('page', 'series'))
        ordering = ['series', 'position']

    def __unicode__(self):
        return "%s - %s (%d)" % (self.page, self.series, self.position)

    def get_previous_page(self):
        if self.position > 1:
            return SeriesPage.objects.get(series=self.series, position=self.position - 1).page

    def get_next_page(self):
        if self.position < self.series.get_num_total():
            return SeriesPage.objects.get(series=self.series, position=self.position + 1).page

    def get_banner_markdown(self):
        if self.series.banner:
            page = self.page
            course_sem = page.course_sem
            raw_text = self.series.banner.text
            text = raw_text % {
                'series_number': self.position,
                'maintainer': '@%s' % page.maintainer,
                'edit_link': page.get_absolute_url() + '/edit',
                'course': course_sem.course,
                'semester': '%s %d' % (course_sem.term.title(), course_sem.year)
            }

            return text
        else:
            return ''


class SeriesBanner(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        app_label = 'wiki'

    def __unicode__(self):
        return self.name
