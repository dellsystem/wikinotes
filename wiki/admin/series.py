from django.contrib import admin

from wiki.models.series import Series, SeriesPage, SeriesBanner


class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Series, SeriesAdmin)
admin.site.register(SeriesPage)
admin.site.register(SeriesBanner)
