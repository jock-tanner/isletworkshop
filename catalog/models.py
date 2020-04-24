import os
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import get_language, gettext_lazy as _
from django_cbrf.models import Currency, Record
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
    weight = models.DecimalField(
        _('weight (g)'),
        max_digits=8,
        decimal_places=3,
        default=Decimal('0.0'),
    )

    # translatable fields
    title_en = models.CharField(
        'title',
        max_length=120,
    )
    title_ru = models.CharField(
        'название',
        max_length=120,
    )
    description_en = models.TextField(
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

    @staticmethod
    def _lang():
        lang = get_language() or settings.LANGUAGE_CODE
        return lang[:2]

    @cached_property
    def title(self):
        return getattr(
            self, 'title_{}'.format(self._lang()), self.title_en
        )

    @cached_property
    def description(self):
        return getattr(
            self, 'description_{}'.format(self._lang()), self.description_en
        )

    @cached_property
    def price(self) -> Decimal:
        if self._lang() == 'ru':
            currency = Currency.objects.filter(iso_char_code='USD').last()
            record = Record.objects.filter(
                currency=currency,
            ).order_by(
                'date',
            ).last()
            # round to 10 roubles, than quantize back to 1 kopeсk/cent
            return (
                round(
                    self.base_price / currency.denomination * record.value, -1
                )
            ).quantize(self.base_price)

        return self.base_price

    @classmethod
    def price_template(cls) -> str:
        return '{} ₽' if cls._lang() == 'ru' else '${}'

    @property
    def local_price(self) -> str:
        return self.price_template().format(self.price)

    def __str__(self):
        return self.title


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
