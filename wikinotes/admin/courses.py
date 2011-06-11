from wikinotes.models.courses import Course
from wikinotes.models.semesters import CourseSemester
from wikinotes.models.real_semesters import Semesters as Semester
from django.contrib import admin

# So that we can update the semesters of a course as we update that course
class CourseSemesterInline(admin.StackedInline):
	model = CourseSemester
	# The number to display should be the number of semesters ...
	extra = Semester.objects.all().count()

class CourseAdmin(admin.ModelAdmin):
	inlines = [CourseSemesterInline]

admin.site.register(Course, CourseAdmin)
