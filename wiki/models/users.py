from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    class Meta:
        app_label = 'wiki'

    user = models.OneToOneField(User)
    twitter = models.CharField(max_length=15, null=True) # max length of a twitter username
    courses = models.ManyToManyField('Course')
    website = models.CharField(max_length=255, null=True)
    bio = models.CharField(max_length=300, null=True)
    facebook = models.CharField(max_length=72, null=True) # apparently that's the limit
    github = models.CharField(max_length=30, null=True) # no idea
    gplus = models.CharField(max_length=21, null=True) # i think, all numbers but char just in case
    major = models.CharField(max_length=100, null=True)
    show_email = models.BooleanField(default=False)

    def start_watching(self, course):
        self.courses.add(course)
        course.increase_num_watchers_by(1)
        course.add_event(self.user, action='started watching')

    def stop_watching(self, course):
        self.courses.remove(course)
        course.increase_num_watchers_by(-1)

    def is_watching(self, course):
        return course in self.courses.all()

    def get_recent_pages(self, n, created=False):
        """
        Return the last n pages that the user has edited.
        """
        pages = []
        i = 0
        history_items = self.user.historyitem_set.order_by('-timestamp')

        # If we want to limit it to pages that the user has created (false by default)
        if created:
            history_items = history_items.filter(action='created')

        for history_item in history_items:
            page = history_item.page
            if page is not None and page not in pages:
                pages.append(page)
                i += 1

                if i == n:
                    break

        return pages

    @models.permalink
    def get_absolute_url(self):
        return ('main_profile', (), {'username': self.user.username})


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Register a handler for the post_save signal
# Otherwise the user profile does not get created
post_save.connect(create_user_profile, sender=User)
