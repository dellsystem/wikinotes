from django.contrib import admin

from wiki.models.pages import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'course_sem')


admin.site.register(Page, PageAdmin)
