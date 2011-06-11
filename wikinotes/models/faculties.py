from django.db import models

class Faculty(models.Model):
	class Meta:
		app_label = 'wikinotes'
	
	# For example, "Agricultural and environmental sciences"
	name = models.CharField(max_length=100)
	# The shorter name. ex "agriculture" "dentistry" "music" "medicine" "science" "arts" "continuing" etc
	slug = models.CharField(max_length=10)
	
	def __unicode__(self):
		return self.name
