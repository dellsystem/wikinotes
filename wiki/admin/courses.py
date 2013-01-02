from django.contrib import admin

from wiki.models.courses import Course, CourseSemester, Professor


class CourseAdmin(admin.ModelAdmin):
    exclude = ('num_watchers', 'latest_activity', 'watchers')


class ProfessorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSemester)
admin.site.register(Professor, ProfessorAdmin)
