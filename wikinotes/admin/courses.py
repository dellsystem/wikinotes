from wikinotes.models.semesters import Semester, CourseSemester
from wikinotes.models.courses import Course
from django.contrib import admin

# So that we can update the semesters of a course as we update that course
class CourseSemesterInline(admin.StackedInline):
	model = CourseSemester
	# The number to display should be the number of semesters ...
	extra = Semester.objects.all().count()

class CourseAdmin(admin.ModelAdmin):
	inlines = [CourseSemesterInline]

admin.site.register(Course, CourseAdmin)
