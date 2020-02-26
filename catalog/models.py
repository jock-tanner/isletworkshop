import os

from django.db import models
from django.utils.translation import get_language, gettext_lazy as _
from model_utils.choices import Choices
from ordered_model.models import OrderedModel
from sorl.thumbnail.fields import ImageField


class Product(models.Model):

    product_types = Choices(
        (1, 'unique', _('One of a kind')),
        (2, 'limited', _('Limited supply')),
        (3, 'unlimited', _('Unlimited supply')),
    )

    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1,
    )
    type = models.PositiveSmallIntegerField(
        _('type'),
        choices=product_types,
        default=product_types.unique,
    )
    base_price = models.DecimalField(
        _('base price'),
        max_digits=12,
        decimal_places=2,
    )

    # translatable fields
    title = models.CharField(
        'title',
        max_length=120,
    )
    title_ru = models.CharField(
        'название',
        max_length=120,
    )
    description = models.TextField(
        'description',
        default='',
        blank=True,
    )
    description_ru = models.TextField(
        'описание',
        default='',
        blank=True,
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('created_at', )

    def __str__(self):
        """ Return the matching translation of the product title. """
        return getattr(self, 'title_'+get_language()[:2], self.title)


class Image(OrderedModel):

    product = models.ForeignKey(
        Product,
        verbose_name=_('product'),
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = ImageField(
        _('image'),
        upload_to='product_images',
    )

    order_with_respect_to = 'product'

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.image.name.split(os.path.sep)[-1]
