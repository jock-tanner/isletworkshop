from typing import Dict

from django.template.base import Node, Variable
from django.template.library import Library
from django.template.exceptions import TemplateSyntaxError

from ..cart import Cart
from catalog.models import Product


register = Library()


class CartNode(Node):

    msg = 'Usage: "{% cart as <new_variable> %}".'

    def __init__(self, parser, token):
        bits = token.split_contents()
        if any([len(bits) != 3, bits[1] != 'as']):
            raise TemplateSyntaxError(self.msg)
        self._name = bits[2]

    def render(self, context):
        request = context.get('request', None)
        if request:
            cart = Cart(request)
            cart_ex = {}
            products = Product.objects.filter(id__in=cart)
            for product in products:
                quantity = cart[product.id]
                cart_ex[product.id] = {
                    'image': (
                        product.images.first()
                        if product.images
                        else None
                    ),
                    'title': product.title,
                    'num_price': product.price,
                    'price': product.local_price,
                    'quantity': quantity,
                    'subtotal': product.price_template().format(
                        product.price * quantity
                    ),
                }
            context[self._name] = cart_ex

        return ''

    def __repr__(self) -> str:
        return '<CartNode>'


class CartQuantityNode(Node):

    msg = 'Usage: "{% cart_quantity <product_id> as <new_variable> %}".'

    def __init__(self, parser, token):
        bits = token.split_contents()
        if any([len(bits) != 4, bits[2] != 'as']):
            raise TemplateSyntaxError(self.msg)
        self._name = bits[3]
        self._product_id = Variable(bits[1])

    def render(self, context):
        request = context.get('request', None)
        if request:
            cart = Cart(request)
            product_id = self._product_id.resolve(context)
            if product_id in cart:
                quantity = str(cart[product_id])
            else:
                quantity = 0
            context[self._name] = quantity

        return ''


@register.tag
def cart(parser, token):
    return CartNode(parser, token)


@register.tag
def cart_quantity(parser, token):
    return CartQuantityNode(parser, token)


@register.filter
def subtotal(cart: Dict) -> str:
    """ Displays subtotal for the cart. """
    return Product.price_template().format(
        sum([n['quantity']*n['num_price'] for i, n in cart.items()])
    )
