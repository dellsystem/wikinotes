from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'wikinotes.views.main.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# For viewing courses and the like
urlpatterns += patterns('views.courses',
    url(r'^courses$', 'index'),
    url(r'^courses/all$', 'all'),
    url(r'^courses/faculty$', 'faculty'), # for browsing by faculty (i.e. lists all the faculties)
    url(r'^(?P<department>\w{4})_(?P<number>[0-9a-zA-Z]{3,5})$', 'overview'),
)

# For viewing, editing and creating pages
urlpatterns += patterns('views.pages',
	url(r'^(?P<department>\w{4})_(?P<number>[0-9a-zA-Z]{3,5})/create/(?P<page_type>[^/]+)/?$', 'create'),
	url(r'^(?P<department>\w{4})_(?P<number>[0-9a-zA-Z]{3,5})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/?$', 'show'),
	url(r'^(?P<department>\w{4})_(?P<number>[0-9a-zA-Z]{3,5})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/edit/?$', 'edit'),
),
