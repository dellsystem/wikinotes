from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

"""
Basic, reusable patterns
"""
faculty = r'(?P<faculty>\w+)'
department = r'(?P<department>\w{4})'
number = '(?P<number>\d{3}D?[12]?)'
course = department + '_' + number
page_type = '(?P<page_type>[^/]+)'
semester = '(?P<term>\w{4,6})-(?P<year>\d{4})'
slug = '(?P<slug>[^/]+)'
page = course + '/' + page_type + '/' + semester + '/' + slug
sha = '(?P<hash>[a-z0-9]{1,40})'

"""
Begin mappings (URLs should be defined in order of descending priority (so highest priority first))
"""
direct_to_view = (
	('main', (
		(('', 'index')),
		(('login', 'login_logout')),
		('recent', 'recent'),
		('recent/(?P<num_days>\d+)', 'recent'),
		('recent/all', 'all_recent'),
		('recent/all/(?P<num_days>\d+)', 'all_recent'),
		('ucp/(?P<mode>\w*)', 'ucp'),
		('user/(?P<username>\w+)', 'profile'),
		('search', 'search'),
		('markdown', 'markdown'),
		('register', 'register')
	)),
	('news', (
		('news', 'main'),
		('news/' + slug, 'view'),
	)),
	('pages', (
		('pages/random', 'random'),
		(course + '/create/' + page_type, 'create'),
		(page, 'show'),
		(page + '/edit', 'edit'),
		(page + '/history', 'history'),
		#(page + '/raw', 'raw'),
		(page + '/commit/' + sha, 'commit'),
		#(page + '/inline', 'inline'),
	))
	('courses', (
		('courses', 'index'),
		('courses/all', 'list_all'),
		('courses/faculty', 'faculty_browse'),
		('courses/department', 'department_browse'),
		('courses/professor', 'professor'),
		('courses/popular', 'popular'),
		('courses/random', 'random'),
		('courses/active', 'active'),
		('courses/get_all', 'get_all'),
		# Redirect department/number to department_number
		(department + '/' + number + '.*', 'remove_slash'),
		(course, 'overview'),
		(course + '/recent', 'recent'),
		(course + '/watch', 'watch'),
		(course + '/series/' + slug, 'series'),
		(course + '/' + semester, 'semester'),
		(course + '/' + page_type, 'category'),
		(department, 'department_overview'),
		(faculty, 'faculty_overview'),
		# The mappings below are kept for "compatibility" but aren't really needed
		('faculty/' + faculty, 'faculty_overview'),
		('department/' + department, 'department_overview'),
	)),
)

# Maps straight from about/history to the static view in main.py
static_urls = {
	'about': ['history', 'licensing', 'platform'], # the index one is implicit
	'contributing': ['moderating', 'development', 'content', 'guidelines'],
	'help': ['copyright', 'formatting'],
}

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
)

"""
Begin code for mapping the mappings
"""

for prefix, filenames in static_urls.iteritems():
	index_url = url(r'^' + prefix + '(?:/overview)?/?$', 'views.main.static', {'mode': prefix, 'page': 'overview'})
	urls = [url(r'^' + prefix + '/' + filename + '/?$', 'views.main.static', {'mode': prefix, 'page': filename}) for filename in filenames]
	urlpatterns += patterns('', index_url, *urls)

for prefix, mapping in direct_to_view:
	urls = [url('^' + regex + '/?$', view, name='%s_%s' % (prefix, view)) for regex, view in mapping]
	urlpatterns += patterns('views.' + prefix, *urls)
