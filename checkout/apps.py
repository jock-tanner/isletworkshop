from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CheckoutConfig(AppConfig):
    name = 'checkout'
    verbose_name = _('Checkout')
