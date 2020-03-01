from django.template.base import Node, Variable
from django.template.library import Library
from django.template.exceptions import TemplateSyntaxError

from ..cart import Cart
from catalog.models import Product


register = Library()


class CartNode(Node):

    def __init__(self, parser, token):
        bits = token.split_contents()
        if any([len(bits) != 3, bits[1] != 'as']):
            raise TemplateSyntaxError(
                'Usage: "{% cart as <new_variable> %}".'
            )
        self._name = bits[2]

    def render(self, context):
        request = context.get('request', None)
        if request:
            cart = Cart(request)
            cart_ex = {}
            products = Product.objects.filter(id__in=cart)
            for product in products:
                cart_ex[product.id] = {
                    'title': product.title,
                    'price': product.base_price,
                    'image': product.images.first() if product.images else None,
                    'quantity': cart[product.id],
                }
            context[self._name] = cart_ex

        return ''

    def __repr__(self) -> str:
        return '<CartNode>'


class CartQuantityNode(Node):

    def __init__(self, parser, token):
        bits = token.split_contents()
        if any([len(bits) != 4, bits[2] != 'as']):
            raise TemplateSyntaxError(
                'Usage: "{% cart_quantity <product_id> %}".'
            )
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
