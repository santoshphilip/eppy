from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^EPlusWebSite/', include('EPlusWebSite.EPlusWeb.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^home/$', 'EPlusWeb.views.home'),
    (r'^idfview/$', 'EPlusWeb.views.idfview'),
    (r'^keys/$', 'EPlusWeb.views.keys'),
    (r'^tmpl/$', 'EPlusWeb.views.tmpl'),
    (r'^allkeys/$', 'EPlusWeb.views.allkeys'),
    (r'^akey/(?P<keyid>\d+)/$', 'EPlusWeb.views.akey'),
    (r'^anobject/(?P<keyid>\d+)/(?P<objid>\d+)/$', 'EPlusWeb.views.anobject'),
    (r'^editfield/(?P<keyid>\d+)/(?P<objid>\d+)/(?P<fieldid>\d+)/$',
                                    'EPlusWeb.views.editfield'),
    (r'^updatefield/(?P<keyid>\d+)/(?P<objid>\d+)/(?P<fieldid>\d+)/$',
                                    'EPlusWeb.views.updatefield'),
# learning stuff
    (r'^learn/$', 'EPlusWeb.learn.learn'),
    (r'^atemplate/$', 'EPlusWeb.learn.atemplate'),
    (r'^anedit/$', 'EPlusWeb.learn.anedit'),
    (r'^formdata/$', 'EPlusWeb.learn.formdata'),
    (r'^edited/$', 'EPlusWeb.learn.edited'),
    
)
