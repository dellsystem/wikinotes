from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'wikinotes.views.main.index'),
    url(r'^courses$', 'wikinotes.views.courses.index'),
    url(r'^courses/all$', 'wikinotes.views.courses.all'),
    # This needs to be improved
    url(r'^(?P<department>\w{4})_(?P<number>\d{3})$', 'wikinotes.views.courses.overview'),
    url(r'^(?P<department>\w{4})_(?P<number>\d{3})/create/(?P<page_type>[^/]+)/?$', 'wikinotes.views.courses.create'),
    url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/?$', 'wikinotes.views.pages.show'),
    url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/edit/?$', 'wikinotes.views.pages.edit'),
    # url(r'^wikinotes/', include('wikinotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
