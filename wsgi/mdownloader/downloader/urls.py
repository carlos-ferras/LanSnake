from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('downloader.views',
    #url(r'^$',include(first.urls)),
    url(r'^$','home'),
    url(r'^downloaded/?','downloaded'),
    url(r'^deskargar/?','deskargar'),
    url(r'^wipe/?','wipeAccount'),
    # Examples:
    # url(r'^$', 'sitio1.views.home', name='home'),
    # url(r'^sitio1/', include('sitio1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
