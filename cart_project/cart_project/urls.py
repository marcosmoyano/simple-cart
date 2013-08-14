from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'stores.views.home', name='home'),
    url(r'^store/', include('stores.urls', namespace="stores")),
    url(r'^checkout/$', 'profiles.views.checkout', name="checkout"),
    url(r'^past-orders/$', 'profiles.views.past_orders', name="past_orders"),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        name="login"),
    url(r'^register/$', 'profiles.views.register', name="register"),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()
