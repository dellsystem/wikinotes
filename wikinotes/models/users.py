from django.db import models
from django.contrib.auth.models import User

# Extends the built-in user model using a OneToOne relationship, sort of
# So we can add the course-watch functionality mainly
# I think this functionality is all we need for the users for now
# Basically an instance of this class is a person watching a course ... yeah
class UserProfile(models.Model):
    class Meta:
        app_label = 'wikinotes'
		
    user = models.OneToOneField(User)
    courses = models.ManyToManyField('Course')
