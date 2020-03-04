from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from catalog.models import Product


class OrderManager(models.Manager):

    @transaction.atomic
    def from_cart(self, cart, user):
        obj = self.model(customer=user)
        obj.save()

        # retrieve all products in one query
        products = {p.id: p for p in Product.objects.filter(id__in=cart)}

        for product_id, quantity in cart.items():
            product = products[product_id]

            # check inventory
            if all([
                product.type != product.product_types.unlimited,
                product.quantity < quantity,
            ]):
                raise ValueError(_('Not enough {}').format(product.title))

            obj.lines.create(
                product=product,
                quantity=quantity,
            )

            # decrease inventory
            if product.type != product.product_types.unlimited:
                product.quantity -= quantity
                product.save()

        return obj


class Order(models.Model):

    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
    )
    paid_at = models.DateTimeField(
        _('paid at'),
        null=True, blank=True,
    )
    cancelled_at = models.DateTimeField(
        _('cancelled at'),
        null=True, blank=True,
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('customer'),
        related_name='orders',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    full_name = models.CharField(
        _('customer\'s full name'),
        max_length=501,
    )
    email = models.EmailField(
        _('customer\'s email address'),
    )

    objects = OrderManager()

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('created_at', )

    def __str__(self):
        return _('Order #{} of {}').__format__(self.id, self.created_at)

    def save(self, *args, **kwargs):
        self.full_name = self.customer.get_full_name()
        self.email = self.customer.email
        super().save(*args, **kwargs)


class OrderLine(models.Model):

    order = models.ForeignKey(
        Order,
        verbose_name=_('order'),
        related_name='lines',
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        'catalog.Product',
        verbose_name=_('product'),
        related_name='order_lines',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(
        'product title',
        max_length=120,
    )
    base_price = models.DecimalField(
        _('base price'),
        max_digits=12,
        decimal_places=2,
    )
    local_price = models.CharField(
        _('local price'),
        max_length=120,
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
    )

    class Meta:
        verbose_name = _('order line')
        verbose_name_plural = _('order lines')

    def save(self, *args, **kwargs):
        self.title = self.product.title
        self.base_price = self.product.base_price
        self.local_price = self.product.local_price
        super().save(*args, **kwargs)
