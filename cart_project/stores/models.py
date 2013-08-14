#-*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


__all__ = ['Cart', 'Store', 'Product', 'Item']


def set_product_location(instance, filename):
    store = instance.store.slug
    return u'{0}/{1}'.format(store, filename)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    creation_date = models.DateTimeField(_('Creation date'))
    checked_out = models.BooleanField(_('Checked out'), default=False)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return u"Cart for {0}".format(self.user)


class Store(models.Model):
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 verbose_name=_('Merchant'),
                                 related_name='stores')
    name = models.CharField(_('Store Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stores:store', kwargs={'slug': self.slug})


class Product(models.Model):
    store = models.ForeignKey(Store,
                              verbose_name=_('Store'))
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)
    description = models.TextField(_('Description'))
    picture = models.ImageField(_('Image'), upload_to=set_product_location,
                                blank=True, null=True)
    price = models.DecimalField(_('Price'),
                                max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stores:product', kwargs={
            'store_slug': self.store.slug,
            'slug': self.slug
        })


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'),
                             related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'Cart Item for product: {0}'.format(self.product.name)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def get_total_price(self):
        return self.total_price
    get_total_price.short_description = _('Total Price')
