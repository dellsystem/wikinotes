from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=50)
	timestamp = models.DateTimeField()
	body = models.TextField()
	summary = models.CharField(max_length=100)
	slug = models.SlugField()

	def __unicode__(self):
		return "%s (%s)" % (self.title, self.timestamp.strftime("%B %d, %Y"))

	def get_url(self):
		return "/news/%s" % self.slug

	def get_num_comments(self):
		return self.blogcomment_set.count()

class BlogComment(models.Model):
	author = models.ForeignKey(User)
	post = models.ForeignKey(BlogPost)
	body = models.TextField()
