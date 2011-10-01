from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.main.index'),
    url(r'^login$', 'views.main.login_logout'),
    url(r'^faculty/(?P<faculty>\w+)$', 'views.courses.faculty_overview'),
    url(r'^department/(?P<department>\w{4})$', 'views.courses.department_overview'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# For viewing courses and the like
urlpatterns += patterns('views.courses',
    url(r'^courses$', 'index'),
    url(r'^courses/all$', 'all'),
    url(r'^courses/faculty$', 'faculty_browse'), # for browsing by faculty (i.e. lists all the faculties and their courses)
    url(r'^courses/department$', 'department_browse'), # for browsing by department
    url(r'^courses/semester$', 'semester'),
    url(r'^courses/professor$', 'professor'),
    url(r'^courses/popular$', 'popular'),
    url(r'^courses/random$', 'random'),
    url(r'^courses/active$', 'active'),
    url(r'^courses/search$', 'search'),
    url(r'^(?P<department>\w{4})_(?P<number>\d{3})$', 'overview'),
    url(r'^(?P<department>\w{4})_(?P<number>\d{3})/watch$', 'watch'),
)

# For viewing, editing and creating pages
urlpatterns += patterns('views.pages',
        url(r'^pages/random$', 'random'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/create/(?P<page_type>[^/]+)/?$', 'create'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/?$', 'show'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/edit/?$', 'edit'),
)
