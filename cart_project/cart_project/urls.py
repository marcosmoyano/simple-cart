from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^checkout$', 'profiles.views.checkout', name="checkout"),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        name="login"),
    url(r'^register/$', 'profiles.views.register', name="register"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('stores.urls', namespace="stores")),
)


if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()
