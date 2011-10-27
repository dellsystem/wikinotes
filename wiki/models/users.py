from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
	class Meta:
		app_label = 'wiki'

	user = models.OneToOneField(User)
	twitter = models.CharField(max_length=15) # max length of a twitter username
	courses = models.ManyToManyField('Course')
	website = models.CharField(max_length=255)
	facebook = models.CharField(max_length=72) # apparently that's the limit

	def start_watching(self, course):
		self.courses.add(course)
		course.num_watchers += 1
		course.add_event(self.user, action='started watching')

	def stop_watching(self, course):
		self.courses.remove(course)
		course.num_watchers -= 1

	def is_watching(self, course):
		return course in self.courses.all()

	def get_url(self):
		return '/user/' + self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Register a handler for the post_save signal
# Otherwise the user profile does not get created
post_save.connect(create_user_profile, sender=User)
