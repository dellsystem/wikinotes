# encoding: utf-8
import os

from django.db import models
from django.contrib.auth.models import User

from wiki.utils.pages import page_types, page_type_choices, get_section_start_end
from wiki.utils.gitutils import Git
from wiki.models.courses import CourseSemester
from wiki.templatetags.wikinotes_markup import wikinotes_markdown


class PageManager(models.Manager):
    """
    This custom manager is defined solely for the purpose of allowing hidden pages
    """
    def visible(self, user, **kwargs):
        if user.is_staff:
            return self.filter(**kwargs)
        else:
            return self.filter(is_hidden=False, **kwargs)


class Page(models.Model):
    class Meta:
        app_label = 'wiki'
        unique_together = ('course_sem', 'slug')
        ordering = ['id']

    objects = PageManager()
    course_sem = models.ForeignKey('CourseSemester')
    subject = models.CharField(max_length=255, null=True, blank=True) # only used for some (most) page types
    link = models.CharField(max_length=255, null=True, blank=True) # remember the max length. only used for some page_types
    page_type = models.CharField(choices=page_type_choices, max_length=20)
    title = models.CharField(max_length=255, null=True, blank=True) # the format of this is determined by the page type
    professor = models.ForeignKey('Professor', null=True, blank=True)
    slug = models.CharField(max_length=50)
    content = models.TextField(null=True) # processed markdown, like a cache
    maintainer = models.ForeignKey(User)
    is_hidden = models.BooleanField(default=False) # for takedown requests

    def can_view(self, user):
        return not self.is_hidden or user.is_staff

    def load_section_content(self, anchor_name):
        """
        This is a really shitty way of doing inline editing, but all the other
        possibilities have been explored and this is the least shitty of them
        all.
        """
        content = self.load_content()
        # Go through the content, looking for headers
        lines = content.splitlines()
        start, end = get_section_start_end(lines, anchor_name)
        section = '\n'.join(lines[start:end])

        return (section, start, end)

    def load_content(self):
        file = open('%scontent.md' % self.get_filepath())
        content = file.read().decode('utf-8')
        file.close()
        return content

    def edit(self, data):
        page_type = page_types[self.page_type]
        # Change the relevant attributes
        for editable_field in page_type.editable_fields:
            setattr(self, editable_field, data[editable_field])

        self.save()
        # THE FOLDER SHOULD NOT HAVE TO BE MOVED!!! NOTHING IMPORTANT NEEDS TO BE CHANGED!!!

    def get_latest_commit(self):
        repo = self.get_repo()
        return repo.get_latest_commit()

    def save_content(self, content, message, username, start=0, end=0):
        # If start and end are valid, use them
        if end > 0:
            saved_content = self.load_content()
            lines = saved_content.splitlines()
            # Ignore edge cases lol
            if end <= len(lines):
                all_lines = lines[:start] + content.splitlines() + lines[end:]
                content = '\r\n'.join(all_lines)

        path = self.get_filepath()
        # If the file doesn't end with a newline, add one
        content += '' if content.endswith('\r\n') else '\r\n'
        self.content = wikinotes_markdown(content)
        self.save()
        repo = self.get_repo()
        filename = '%scontent.md' % path
        file = open(filename, 'wt')
        file.write(content.encode('utf-8'))
        file.close()

        repo.commit(message, username, '')

    def __unicode__(self):
        return '%s - %s' % (self.get_title(), self.course_sem)

    def get_filepath(self):
        return "wiki/content%s/" % self.get_absolute_url()

    def get_type(self):
        return page_types[self.page_type]

    def get_title(self):
        if not self.title:
            return self.subject
        else:
            return self.title

    def get_metadata(self):
        metadata = {} # Key: name, value: content
        for field in self.get_type().get_metadata_fields():
            content = self.__getattribute__(field)
            if content:
                metadata[field] = content
        return metadata

    def get_absolute_url(self):
        course = self.course_sem.course
        return "%s/%s/%s-%s/%s" % (course.get_absolute_url(), self.page_type, self.course_sem.term, self.course_sem.year, self.slug)

    # The method can't be solely on the page type itelf, since it doesn't know what course it's for
    def get_type_url(self):
        return self.get_type().get_url(self.course_sem.course)

    # Returns a Git object
    def get_repo(self):
        return Git(self.get_filepath())
