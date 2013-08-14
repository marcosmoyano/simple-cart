from django.conf.urls import patterns, url

urlpatterns = patterns(
    'stores.views',
    url(r'^(?P<slug>[\w-]+)/$', 'store', name='store'),
    url(r'^(?P<store_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        'product', name='product'),
    url(r'^(?P<store_slug>[\w-]+)/(?P<slug>[\w-]+)/add/$',
        'add_to_cart', name='add_to_cart'),
    url(r'^(?P<store_slug>[\w-]+)/(?P<slug>[\w-]+)/update/$',
        'update_cart', name='update_cart'),

)
