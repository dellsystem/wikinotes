from django.contrib import admin

from wiki.models.series import Series, SeriesPage


class SeriesPageInline(admin.TabularInline):
    model = SeriesPage


class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesPageInline]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Series, SeriesAdmin)
