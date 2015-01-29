<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from django.conf.urls import patterns, include, url
=======
=======
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59
=======
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59
"""from django.conf.urls.defaults import *"""
from django.conf.urls import patterns, include, url
#from django.views.generic.simple import direct_to_template
#from django.contrib import admin
<<<<<<< HEAD
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59


urlpatterns = patterns('',
    url(r'', include('downloader.urls')),
=======

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('downloader.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59
)