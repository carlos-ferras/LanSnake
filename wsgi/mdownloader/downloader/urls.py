from django.conf.urls import patterns, include, url

urlpatterns = patterns('downloader.views',
    url(r'^$','home'),
    url(r'^data/?','data'),
    url(r'^deskargar/?','deskargar'),
    url(r'^wipe/?','wipeAccount'),
)
