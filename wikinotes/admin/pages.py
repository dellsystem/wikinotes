from wikinotes.models.pages import PageType
from django.contrib import admin

class PageTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'to_str', 'need_date')

admin.site.register(PageType, PageTypeAdmin)
