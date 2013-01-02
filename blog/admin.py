from blog.models import BlogPost
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(BlogPost, BlogAdmin)
