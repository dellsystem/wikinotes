from wikinotes.models.pages import PageType, Page
from django.contrib import admin

class PageTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'to_str', 'need_date')

admin.site.register(PageType, PageTypeAdmin)

admin.site.register(Page)
