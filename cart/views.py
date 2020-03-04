from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin

from .cart import Cart
from .forms import CartAddForm, CartRemoveForm
from catalog.models import Product


class CartView(TemplateView):
    template_name = 'cart.html'

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        # do less queries per hit
        products = {p.id: p for p in Product.objects.filter(id__in=cart)}

        for k, v in request.POST.items():

            if k.startswith('quantity_id'):
                product_id = int(k.split('_id')[1])
                quantity = int(v)

                if quantity == 0:
                    del cart[product_id]
                    continue

                product = products[product_id]
                if product.type == product.product_types.unlimited:
                    cart[product_id] = quantity
                else:
                    # check inventory
                    cart[product_id] = min(quantity, product.quantity)
                continue

            if k.startswith('remove_id'):
                product_id = int(k.split('_id')[1])
                del cart[product_id]
                break

        return self.get(request, *args, **kwargs)


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
