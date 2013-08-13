from django.conf.urls import patterns, url

urlpatterns = patterns(
    'stores.views',
    url(r'^$', 'home', name='home'),
    url(r'^(?P<slug>[\w-]+)/$', 'store', name='store'),
    url(r'^(?P<store_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        'product', name='product'),
    url(r'^(?P<store_slug>[\w-]+)/(?P<slug>[\w-]+)/add/$',
        'add_to_cart', name='add_to_cart'),

)
