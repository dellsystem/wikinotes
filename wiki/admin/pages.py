from django.contrib import admin

from wiki.models.pages import Page, ExternalPage


class PageAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'page_type', 'course_sem')


admin.site.register(Page, PageAdmin)
admin.site.register(ExternalPage)
