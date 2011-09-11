from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'wikinotes.views.main.index'),
    url(r'^courses$', 'wikinotes.views.courses.index'),
    url(r'^courses/all$', 'wikinotes.views.courses.all'),
    url(r'^(?P<department>\w{4})_(?P<number>\d{3})$', 'wikinotes.views.courses.overview'),
    # url(r'^wikinotes/', include('wikinotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
