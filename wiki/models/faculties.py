from django.db import models

class Faculty(models.Model):
	class Meta:
		app_label = 'wiki'

	# Ex: "Agricultural and environmental sciences"
	name = models.CharField(max_length=100)
	# For use in URLs. Ex: "agriculture" "dentistry" "music" "medicine" "science" "arts" "continuing" etc
	slug = models.CharField(max_length=15)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('courses_faculty_overview', (), {'faculty': self.slug})

	def get_image(self):
		return "/static/img%s.png" % self.get_absolute_url()
