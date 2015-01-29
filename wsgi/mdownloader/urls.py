<<<<<<< HEAD
<<<<<<< HEAD
from django.conf.urls import patterns, include, url
=======
=======
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59
"""from django.conf.urls.defaults import *"""
from django.conf.urls import patterns, include, url
#from django.views.generic.simple import direct_to_template
#from django.contrib import admin
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59


urlpatterns = patterns('',
    url(r'', include('downloader.urls')),
)