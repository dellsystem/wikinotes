from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wikinotes/', include('wikinotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Viewing a specific user
    (r'^user/(?P<username>\w+)$', 'users.views.user'),
    
    # Viewing a specific course
    (r'^(?P<department>\w+)_(?P<number>\d+)$', 'courses.views.course'),
    
    # Viewing a specific department
    (r'^(?P<department>\w+)$', 'departments.views.department'),
    
)
