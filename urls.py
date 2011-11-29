from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'views.main.index'),
	url(r'^login$', 'views.main.login_logout'),
	url(r'^recent$', 'views.main.recent'),
	url(r'^recent/all$', 'views.main.recent', {'show_all': True}),
	url(r'^recent/(?P<num_days>\d+)$', 'views.main.recent'),
	url(r'^recent/all/(?P<num_days>\d+)$', 'views.main.recent', {'show_all': True}), # lol fix this
	url(r'^faculty/(?P<faculty>\w+)$', 'views.courses.faculty_overview'),
	url(r'^department/(?P<department>\w{4})$', 'views.courses.department_overview'),
	url(r'^user/(?P<username>\w+)$', 'views.main.profile'),
	url(r'^ucp/?(?P<mode>\w*)$', 'views.main.ucp'),

	# Registration stuff
	url(r'^register$', 'views.main.register'),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

# Can be made cleaner
urlpatterns += patterns('views.about',
	url(r'^about$', 'index'),
	url(r'^about/overview$', 'overview'),
	url(r'^about/history$', 'history'),
	url(r'^about/licensing$', 'licensing'),
	url(r'^about/platform$', 'platform'),
)

urlpatterns += patterns('views.help',
	url(r'^help$', 'index'),
	url(r'^help/copyright$', 'copyright'),
)

urlpatterns += patterns('views.contributing',
	url(r'^contributing$', 'index'),
	url(r'^contributing/moderating$', 'moderating'),
	url(r'^contributing/development$', 'development'),
	url(r'^contributing/representatives$', 'representatives'),
	url(r'^contributing/content$', 'content'),
	url(r'^contributing/guidelines$', 'guidelines'),
)

# For viewing courses and the like
urlpatterns += patterns('views.courses',
	url(r'^courses$', 'index'),
	url(r'^courses/all$', 'list_all'),
	url(r'^courses/faculty$', 'faculty_browse'), # for browsing by faculty (i.e. lists all the faculties and their courses)
	url(r'^courses/department$', 'department_browse'), # for browsing by department
	url(r'^courses/semester$', 'semester'),
	url(r'^courses/professor$', 'professor'),
	url(r'^courses/popular$', 'popular'),
	url(r'^courses/random$', 'random'),
	url(r'^courses/active$', 'active'),
	url(r'^courses/search$', 'search'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})$', 'overview'),
	#url(r'^(?P<department>\w{4})_(?P<number>\d{3})/recent$', 'recent'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/watch$', 'watch'),
)

# For viewing, editing and creating pages
urlpatterns += patterns('views.pages',
		url(r'^pages/random$', 'random'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/create/(?P<page_type>[^/]+)$', 'create'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)$', 'show'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/edit$', 'edit'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/history$', 'history'),
	url(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<page_type>[^/]+)/(?P<term>\w{4,6})-(?P<year>\d{4})/(?P<slug>[^/]+)/commit/(?P<hash>[a-z0-9]{1,40})$', 'commit'), # viewing a particular commit etc
)
