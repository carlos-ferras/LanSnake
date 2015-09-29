from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import serve

urlpatterns = patterns('downloader.views',
    url(r'^$','home'),
    url(r'^close/$','out'),
    url(r'^account/asd34y91lk0/data/?','data'),
    url(r'^account/asd34y91lk0/profile/?','deskargar'),
    url(r'^account/asd34y91lk0/wipe/?','wipeAccount'),
    url(r'^staticfiles/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}),
)
