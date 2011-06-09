from django.db import models
from courses.models import Course
from django.contrib.auth.models import User

# Extends the built-in user model using a OneToOne relationship, sort of
# So we can add the course-watch functionality mainly
class UserCourses(models.Model):
	courses = models.ManyToManyField(Course)
	user = models.ForeignKey(User, unique=True)
