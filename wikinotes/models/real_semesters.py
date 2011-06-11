from django.db import models
from wikinotes.utils.semesters import get_possible_terms, get_possible_years

# Kind of like an enum in java lol
class Semesters(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	# Can be Summer, Spring or Winter
	term = models.CharField(max_length=6, choices=get_possible_terms())
	year = models.IntegerField(max_length=4, choices=get_possible_years())
	
	def __unicode__(self):
		return "%s (%d)" % (self.term, self.year)
