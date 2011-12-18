from wiki.models.series import Series, SeriesPage
from django.contrib import admin

class SeriesPageInline(admin.TabularInline):
	model = SeriesPage

class SeriesAdmin(admin.ModelAdmin):
	inlines = [SeriesPageInline]
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Series, SeriesAdmin)
#admin.site.register(SeriesPage)
