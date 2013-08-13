#-*- coding: utf-8 -*-

from django.contrib import admin
from .models import Store, Product, Item, Cart
from profiles.models import StoreUser


__all__ = ['StoreAdmin', 'ProductAdmin', 'ItemAdmin', 'CartAdmin']


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date', 'checked_out')
    list_filter = ('checked_out', )

    def queryset(self, request):
        # We could (and should) denormalize this
        return Cart.objects.filter(
            items__product__store__merchant=request.user
        )


class StoreAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}

    def queryset(self, request):
        return Store.objects.filter(merchant=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "merchant":
            kwargs["queryset"] = StoreUser.objects.filter(id=request.user.id)
        return super(StoreAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}

    def queryset(self, request):
        return Product.objects.filter(store__merchant=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store":
            kwargs["queryset"] = Store.objects.filter(merchant=request.user)
        return super(ProductAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class ItemAdmin(admin.ModelAdmin):

    list_display = ('cart', 'quantity', 'get_total_price')

    def queryset(self, request):
        return Item.objects.filter(product__store__merchant=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(
                store__merchant=request.user
            )
        return super(ItemAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
