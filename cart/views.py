from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormMixin

from .cart import Cart
from .forms import CartAddForm, CartRemoveForm
from catalog.models import Product


class CartAddView(FormMixin, View):
    form_class = CartAddForm

    def post(self, request, product_id: int, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.add(product, form.cleaned_data['quantity'])
            return HttpResponseRedirect(form.cleaned_data['next'])
        else:
            return HttpResponseBadRequest()


class CartRemoveView(FormMixin, View):
    form_class = CartRemoveForm

    def post(self, request, product_id: int, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.remove(product)
            return HttpResponseRedirect(form.cleaned_data['next'])
        else:
            return HttpResponseBadRequest()
