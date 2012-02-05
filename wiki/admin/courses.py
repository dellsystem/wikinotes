from wiki.models.courses import Course, CourseSemester, Professor
from django.contrib import admin

class CourseAdmin(admin.ModelAdmin):
	exclude = ('num_watchers', 'latest_activity', 'watchers')

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSemester)
admin.site.register(Professor)
