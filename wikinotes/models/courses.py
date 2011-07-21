from django.db import models
from wikinotes.models.departments import Department
from wikinotes.utils.semesters import get_possible_terms, get_possible_years, get_possible_semesters, get_current_semester
from wikinotes.models.professors import Professor
from wikinotes.models.users import UserProfile
from wikinotes.models.pages import Page

class SemesterField(models.Field):
	description = 'A semester in the format [Term] [Year]'
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 11 # That is the length of 'Winter 2011' and is the longest possible
		kwargs['choices'] = get_possible_semesters()
		super(SemesterField, self).__init__(*args, **kwargs)
	def get_internal_type(self):
		return 'CharField'

class Course(models.Model):

    class Meta:
        app_label = 'wikinotes'

    department = models.ForeignKey(Department)
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    credits = models.IntegerField()
	
	# The department + number should be shown
    def __unicode__(self):
	    return "%s %d" % (self.department, self.number)
	
    def get_name(self):
	    return self.name
	
    def get_description(self):
	    return self.description
	
    def get_credits(self):
	    return self.credits
	
    def get_num_watchers(self):
	    return UserProfile.objects.filter(courses__name__contains=self.name).count()
	
    def get_num_pages(self):
	    num_pages = Page.objects.filter(course_semester__course=self).count()
	    return num_pages
	
    def is_user_watching(self, user):
	    try:
		    UserProfile.objects.filter(user=user, courses__name__contains=self.name)
		    return True
	    except UserProfile.DoesNotExist:
			return False
	
    def get_current_profs(self):
        try:
			return CourseSemester.objects.get(course=self, semester=get_current_semester()).professors.all()
        except CourseSemester.DoesNotExist:
			# If the prof doesn't exist, return None, the template will take care of it
			return None

class CourseSemester(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	course = models.ForeignKey(Course)
	semester = SemesterField()
	professors = models.ManyToManyField(Professor, blank=True)
	
	# So like B+ A- etc. Should be optional
	course_avg = models.CharField(max_length=2, blank=True)
	def __unicode__(self):
		return "%s, %s" % (self.course, self.semester)
	def get_term(self):
		# Just return all but the last five characters
		return self.semester[:-5]
	def get_year(self):
		# Just return the last four digits
		return int(self.semester[-4:])
