#-*- coding: utf-8 -*-

from django.contrib import admin
from .models import Store, Product, Item, Cart
from profiles.models import StoreUser


__all__ = ['StoreAdmin', 'ProductAdmin', 'ItemAdmin', 'CartAdmin']


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date', 'checked_out')
    list_filter = ('checked_out', )

    def queryset(self, request):
        if request.user.is_superuser:
            return Cart.objects.all()
        # We could (and should) denormalize this
        return Cart.objects.filter(
            items__product__store__merchant=request.user
        )


class StoreAdmin(admin.ModelAdmin):

    list_display = ('name', 'merchant')
    prepopulated_fields = {"slug": ("name",)}

    def queryset(self, request):
        if request.user.is_superuser:
            return Store.objects.all()
        return Store.objects.filter(merchant=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            qs = {}
        else:
            if db_field.name == "merchant":
                qs = {'id': request.user.id}
        kwargs["queryset"] = StoreUser.objects.filter(**qs)
        return super(StoreAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store')
    prepopulated_fields = {"slug": ("name",)}

    def queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(store__merchant=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            qs = {}
        else:
            if db_field.name == "store":
                qs = {'merchant': request.user}
        kwargs["queryset"] = Store.objects.filter(**qs)
        return super(ProductAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class ItemAdmin(admin.ModelAdmin):

    list_display = ('cart', 'quantity', 'get_total_price')

    def queryset(self, request):
        if request.user.is_superuser:
            return Item.objects.all()
        return Item.objects.filter(product__store__merchant=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            qs = {}
        else:
            if db_field.name == "product":
                qs = {'store__merchant': request.user}
        kwargs["queryset"] = Product.objects.filter(**qs)
        return super(ItemAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
