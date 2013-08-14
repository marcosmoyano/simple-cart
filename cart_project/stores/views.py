#-*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Store, Product, Item
from .forms import AddToCartForm, UpdateCartForm
from .cart import UserCart


def home(request, template="stores/home.html"):
    """ Home View. List all available stores """
    stores = Store.objects.all()
    return render(request, template, {'stores': stores})


def store(request, slug=None, template="stores/store.html"):
    """ List all pruducts for the given Store """
    store = get_object_or_404(Store, slug=slug)
    products = store.product_set.all()
    return render(request, template, {'store': store, 'products': products})


def product(request, store_slug=None, slug=None,
            template="stores/product.html"):
    """ Pruduct Detail Page """
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, store__slug=store_slug, slug=slug)
    form = AddToCartForm()
    return render(request, template, {'store': store,
                                      'product': product,
                                      'form': form})


@login_required
def add_to_cart(request, store_slug=None, slug=None,
                template="stores/add.html"):
    """ Add to Cart handling view. Updates or creates a new Cart """
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, store__slug=store_slug, slug=slug)
    form = AddToCartForm(request.POST or None)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        cart = UserCart(request)
        cart.add(product, quantity)
        messages.info(request, 'The product has been added to your cart')
        return HttpResponseRedirect(reverse('stores:store', kwargs={
            'slug': store.slug,
        }))
    return render(request, template, {'store': store,
                                      'product': product,
                                      'form': form})


@login_required
def update_cart(request, store_slug=None, slug=None,
                template="stores/update.html"):
    """ Update Cart (or create) for the given Product """
    cart = UserCart(request)
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, store=store, slug=slug)
    item = Item.objects.get(product=product, cart=cart.cart)
    form = UpdateCartForm(request.POST or None,
                          initial={'quantity': item.quantity})
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        cart = UserCart(request)
        cart.update(product, quantity)
        messages.info(request, 'The cart has been updated')
        return HttpResponseRedirect(reverse('checkout'))
    return render(request, template, {'store': store,
                                      'product': product,
                                      'form': form})
