from django.db import models
from django.db.models import fields

class Keyword(models.Model):
	class Meta:
		app_label = 'wiki'
		unique_together = (("keyword", "commit", "page"))
	hash = models.CharField(max_length=40, primary_key=True)
	page = models.IntegerField()
	keyword = models.CharField(max_length=120) #reasonable length for longest word
	commit = models.CharField(max_length=100)
	frequency = models.IntegerField(default=0)
	date = models.IntegerField()
	head = models.IntegerField()

class KeywordLocation(models.Model):
	class Meta:
		app_label = 'wiki'

	k_id = models.CharField(max_length=32, primary_key=True)
	keyword_hash = models.CharField(max_length=40)
	word = models.CharField(max_length=120)
	page = models.IntegerField()
	line_num = models.IntegerField()
	pos = models.IntegerField()
	head = models.IntegerField()
	head_line_num = models.IntegerField(null=True)
	temp = models.IntegerField(null=True)

#not actually a model
class Result():

	def __init__(self):
		self.page = None
		self.preview_text = ""
		self.commits_mentioned = []
		self.terms = []
		self.commits_hidden = 0

