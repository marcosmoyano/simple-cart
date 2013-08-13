#-*- coding: utf-8 -*-

import datetime
from django.utils.translation import ugettext_lazy as _
from .models import Cart, Item


__all__ = ['UserCart', ]


class UserCart(object):
    def __init__(self, request):
        """Initializes the User's Cart creating one if the user has no Cart"""
        user = request.user
        if user:
            try:
                cart = Cart.objects.get(user=user, checked_out=False)
            except Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        """ Iterate over the Cart items """
        for item in self.cart.items.all():
            yield item

    def new(self, request):
        """ Create and return a new Cart instance """
        cart = Cart(creation_date=datetime.datetime.now(),
                    user=request.user)
        cart.save()
        return cart

    def add(self, product, quantity=1):
        """ Add a product to the User's Cart instance """
        try:
            item = Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except Item.DoesNotExist:
            item = Item(cart=self.cart,
                        product=product,
                        quantity=quantity
            )
            item.save()
        else:
            raise ValueError(_('Item Already Exist'))

    def remove(self, product):
        """ Remove a product from the User's Cart instance """
        try:
            item = Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except Item.DoesNotExist:
            raise ValueError(_('Item Does not Exist'))
        else:
            item.delete()

    def update(self, product, quantity):
        """ Update the quantity of a product from the User's Cart instance """
        try:
            item = Item.objects.update(
                cart=self.cart,
                product=product,
                quantity=quantity
            )
        except Item.DoesNotExist:
            raise ValueError(_('Item Does not Exist'))

    def clear(self):
        """ Clear the User's Cart. Removes all items """
        for item in self.cart.items.all():
            item.delete()

    def is_empty(self):
        """ Return True if the Cart is empty """
        return self.cart.items.count() == 0

    def total(self):
        """ Get the Cart total """
        return sum([item.total_price for item in self.cart.items.all()])

    def checkout(self):
        """ Close the current Cart """
        # Payment should go through here.
        self.cart.checked_out = True
        self.cart.save()
        return True
