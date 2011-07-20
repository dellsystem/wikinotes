from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import logout

# Wikinotes stuff
urlpatterns = patterns('wikinotes.views',
	(r'^$', 'other.index'), # can't think of a better name
	(r'^user/(?P<username>\w+)/*$', 'users.profile'),
	(r'^logout/*$', logout), # for now
	(r'^(?P<department>\w{4})_(?P<number>\d{3})/*$', 'courses.overview'),
	(r'^(?P<department>\w{4})_(?P<number>\d{3})/watch/*$', 'courses.watch'),
	(r'^(?P<department>\w{4})_(?P<number>\d{3})/create/(?P<page_type>\w+)/*$', 'pages.create'),
	(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<term>\w+)-(?P<year>\d{4})/(?P<page_type>\w+)/(?P<slug>[^/]*)/*$', 'pages.view'),
	(r'^(?P<department>\w{4})_(?P<number>\d{3})/(?P<term>\w+)-(?P<year>\d{4})/(?P<page_type>\w+)/(?P<slug>[^/]*)/edit/*$', 'pages.edit'),
	(r'^(?P<department>\w{4})/*$', 'departments.overview'),
	(r'^(?P<faculty_slug>\w+)/*$', 'faculties.overview'),
)
