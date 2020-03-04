from collections import defaultdict

from django.conf import settings
from catalog.models import Product


class Cart:
    """ Shopping cart. """

    def __init__(self, request):
        self._session = request.session
        cart = self._session.get(settings.CART_SESSION_KEY, None)
        if cart is None:
            cart = self._session[settings.CART_SESSION_KEY] = defaultdict(int)
        self._cart = cart
        self._save()

    def add(self, product: Product, quantity: int):
        """
        Puts the product into the cart.

        :param product: the product. It is assumed that the Python type of
          Product.id is integer,
        :param quantity: the product's quantity,
        """
        self._cart[product.id] = min(
            self._cart[product.id] + quantity, product.quantity,
        )

        if self._cart[product.id] == 0:
            self._cart.pop(product.id, None)

        self._save()

    def remove(self, product: Product):
        """
        Removes the product from the cart.

        :param product: the product to remove.
        """
        self._cart.pop(product.id, None)
        self._save()

    def _save(self):
        self._session.modified = True

    def __iter__(self):
        for i in self._cart:
            yield i

    def __getitem__(self, product_id):
        return self._cart[product_id]

    def __setitem__(self, product_id, quantity):
        self._cart[product_id] = quantity

    def __delitem__(self, product_id):
        del self._cart[product_id]
