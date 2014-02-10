from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

"""
Basic, reusable patterns
"""
faculty = r'(?P<faculty>\w+)'
department = r'(?P<department>\w{4})'
number = '(?P<number>\d{3}[DNJ]?[123]?)'
course = department + '_' + number
page_type = '(?P<page_type>[^/]+)'
semester = '(?P<term>\w{4,6})-(?P<year>\d{4})'
slug = '(?P<slug>[^/]+)'
page = course + '/' + page_type + '/' + semester + '/' + slug
sha = '(?P<hash>[a-z0-9]{40})'
professor = '(?P<professor>[a-z-]*)'

"""
Begin mappings (URLs should be defined in order of descending priority (so highest priority first))
"""
direct_to_view = (
    ('main', (
        ('login', 'login_logout'),
        ('recent', 'recent'),
        ('recent/(?P<num_days>\d+)', 'recent'),
        ('recent/all', 'all_recent'),
        ('recent/all/(?P<num_days>\d+)', 'all_recent'),
        ('ucp', 'ucp'),
        ('ucp/(?P<mode>\w*)', 'ucp'),
        ('users/(?P<username>\w+)', 'profile'),
        ('users/(?P<username>\w+)/contributions', 'contributions'),
        ('search', 'search'),
        ('markdown', 'markdown'),
        ('register', 'register')
    )),
    ('messages', (
        ('messages', 'inbox'),
        ('messages/inbox', 'inbox'),
        ('messages/outbox', 'outbox'),
        ('messages/compose', 'compose'),
        ('messages/view/(?P<message_id>\d+)', 'view'),
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
        (page + '/print', 'printview'),
        #(page + '/raw', 'raw'),
        (page + '/commit/' + sha, 'commit'),
        #(page + '/inline', 'inline'),
    )),
    ('courses', (
        ('courses', 'index'),
        ('courses/create', 'create'),
        ('courses/all', 'all_browse'),
        ('courses/faculty', 'faculty_browse'),
        ('courses/department', 'department_browse'),
        ('courses/professor', 'professor_browse'),
        ('courses/popular', 'popular_browse'),
        ('courses/random', 'random'),
        ('courses/active', 'active_browse'),
        ('courses/get_all', 'get_all'),
        # Redirect department/number to department_number
        (department + '/' + number + '.*', 'remove_slash'),
        (course, 'overview'),
        (course + '/recent', 'recent'),
        (course + '/watch', 'watch'),
        (course + '/' + semester, 'semester_overview'),
        (course + '/' + page_type, 'category_overview'),
        (department, 'department_overview'),
        ('faculty/' + faculty, 'faculty_overview'),
        ('professor/' + professor, 'professor_overview'),
    )),
)

# Maps straight from about/history to the static view in main.py
static_urls = {
    'about': ['history', 'licensing', 'platform'], # the index one is implicit
    'contributing': ['moderating', 'development', 'content', 'guidelines'],
    'help': ['copyright', 'formatting', 'lexers'],
}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

"""
Begin code for mapping the mappings
"""

# The index view has to be done separately
urlpatterns += patterns('',
    url(r'^$', 'views.main.index', name='home'),
)

for prefix, filenames in static_urls.iteritems():
    index_url = url(r'^' + prefix + '(?:/overview)?/$', 'views.main.static',
        {'mode': prefix, 'page': 'overview'}, name=prefix)
    urls = [url(r'^' + prefix + '/' + filename + '/$', 'views.main.static',
        {'mode': prefix, 'page': filename},
        name=prefix + '_' + filename) for filename in filenames]
    urlpatterns += patterns('', index_url, *urls)

for prefix, mapping in direct_to_view:
    urls = [url('^' + regex + '/$', view, name='%s_%s' % (prefix, view)) for regex, view in mapping]
    urlpatterns += patterns('views.' + prefix, *urls)
