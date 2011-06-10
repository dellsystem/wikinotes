from django.db import models
from courses.models import Course
from django.contrib.auth.models import User

# Extends the built-in user model using a OneToOne relationship, sort of
# So we can add the course-watch functionality mainly
# I think this functionality is all we need for the users for now
# Basically an instance of this class is a person watching a course ... yeah
class CourseWatcher(models.Model):
	course = models.ManyToManyField(Course)
	user = models.ForeignKey(User, unique=True)
