from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from wiki.models.history import HistoryItem
from wiki.utils.currents import current_year, current_term


class Course(models.Model):
    department = models.ForeignKey('Department')
    number = models.CharField(max_length=5, verbose_name="Course number")
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    credits = models.DecimalField(max_digits=2, decimal_places=1,
        verbose_name="Number of credits") # Can be 4.5
    watchers = models.ManyToManyField(User, null=True, blank=True)
    # The latest_activity field makes it easier to sort and stuff ... not strictly necessary
    latest_activity = models.ForeignKey('HistoryItem',
        related_name='latest_course', null=True, blank=True)
    num_watchers = models.IntegerField(default=0) # caches it basically
    url_fields = {
        'department': 'department__short_name__iexact',
        'number': 'number',
    }

    class Meta:
        app_label = 'wiki'
        ordering = ['department__short_name', 'number']

    def __unicode__(self):
        return "%s %s" % (self.department.short_name, self.number)

    def get_absolute_url(self):
        return reverse('courses_overview', args=self.get_url_args())

    def increase_num_watchers_by(self, i):
        self.num_watchers += i
        self.save()

    def get_current_semester(self):
        try:
            return CourseSemester.objects.get(course=self, term=current_term, year=current_year)
        except CourseSemester.DoesNotExist:
            return None

    def get_url_args(self):
        return (self.department.pk, self.number)

    def get_recent_url(self):
        return reverse('courses_recent', args=self.get_url_args())

    def get_watch_url(self):
        return reverse('courses_watch', args=self.get_url_args())

    def num_pages(self):
        count = 0
        course_sems = self.coursesemester_set.all()
        for sem in course_sems:
            num_pages = sem.page_set.count()
            count += num_pages
        return count

    # Use this for adding an event to a course
    def add_event(self, user=None, action=None, page=None, message='',
        hexsha=None):
        new_item = HistoryItem(user=user, action=action, page=page, course=self,
            message=message, hexsha=hexsha)
        new_item.save()
        self.latest_activity = new_item
        self.save()

    # Get history items for this course; limited to 5 when called from the template
    # Set to 0 for no limit
    def recent_activity(self, limit=5):
        course_history = HistoryItem.objects.filter(course=self).order_by('-timestamp')
        if limit > 0:
            return course_history[:limit]
        else:
            return course_history


class CourseSemester(models.Model):
    course = models.ForeignKey('Course')
    evaluation = models.TextField(null=True, blank=True)
    professors = models.ManyToManyField('Professor', null=True, blank=True)
    midterm_info = models.TextField(null=True, blank=True)
    final_info = models.TextField(null=True, blank=True)
    readings = models.TextField(null=True, blank=True)
    term = models.CharField(max_length=6) # Winter/Summer etc
    year = models.IntegerField(max_length=4) # Because ... yeah
    url_fields = {
        'department': 'course__department__short_name__iexact',
        'number': 'course__number',
        'term': 'term',
        'year': 'year',
    }

    class Meta:
        app_label = 'wiki'
        unique_together = ('term', 'year', 'course')

    def __unicode__(self):
        return "%s (%s %d)" % (self.course, self.term.title(), self.year)

    def get_absolute_url(self):
        url_args = self.course.get_url_args() + (self.term, self.year)
        return reverse('courses_semester', args=url_args)

    def get_semester(self):
        # For printing out. Returns Term year
        return "%s %d" % (self.term.title(), self.year)

    def get_slug(self):
        return "%s-%s" % (self.term, self.year)


class Professor(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    link = models.URLField(blank=True, null=True)
    url_fields = {
        'professor': 'slug',
    }

    class Meta:
        app_label = 'wiki'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses_professor_overview', args=[self.slug])
