from django.db import models


class Series(models.Model):
    class Meta:
        app_label = 'wiki'
        unique_together = (('course', 'position'), ('course', 'slug'))
        verbose_name_plural = 'Series'

    course = models.ForeignKey('Course')
    name = models.CharField(max_length=255)
    position = models.IntegerField()
    slug = models.SlugField()

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.course)

    def get_absolute_url(self):
        return '%s/series/%s' % (self.course.get_absolute_url(), self.slug)

    def get_num_total(self):
        return self.seriespage_set.count()


class SeriesPage(models.Model):
    class Meta:
        app_label = 'wiki'
        # Each page can only be in a series once, each series can have only one page per position
        unique_together = (('position', 'series'), ('page', 'series'))
        ordering = ['series', 'position']

    page = models.ForeignKey('Page')
    series = models.ForeignKey('Series')
    position = models.IntegerField('position')

    def __unicode__(self):
        return "%s - %s (%d)" % (self.page, self.series, self.position)

    def get_previous_page(self):
        if self.position > 1:
            return SeriesPage.objects.get(series=self.series, position=self.position - 1).page

    def get_next_page(self):
        if self.position < self.series.get_num_total():
            return SeriesPage.objects.get(series=self.series, position=self.position + 1).page
