# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

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
