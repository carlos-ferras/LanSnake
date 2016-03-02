# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url,include
from django.conf import settings
from . import views

app_name='downloader'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.data, name='data'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^myaccount/profile/$', views.download, name='download'),
    url(r'^myaccount/messages/$', views.wipeAccount, name='wipe'),
]