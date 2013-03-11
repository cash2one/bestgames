from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ContentEngine.views.home', name='home'),
    # url(r'^ContentEngine/', include('ContentEngine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'site/','site/'),
    url(r'^$',include('api.urls')),
    url(r'sina/',include('api.urls')),
    url(r'token/',include('api.urls')),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_PATH})
)

urlpatterns += staticfiles_urlpatterns()


