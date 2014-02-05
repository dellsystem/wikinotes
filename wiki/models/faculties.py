from django.core.urlresolvers import reverse
from django.db import models


class Faculty(models.Model):
    # Ex: "Agricultural and environmental sciences"
    name = models.CharField(max_length=100)
    # For use in URLs. Ex: "agriculture" "dentistry" "music" "medicine" "science" "arts" "continuing" etc
    slug = models.CharField(max_length=15)

    class Meta:
        app_label = 'wiki'
        verbose_name_plural = "Faculties"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses_faculty_overview', args=[self.slug])

    def get_image(self):
        return "/static/img/faculty/%s.png" % self.slug
