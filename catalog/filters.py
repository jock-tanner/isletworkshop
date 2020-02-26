from django.utils.translation import gettext_lazy as _
import django_filters as filters


class ProductFilterSet(filters.FilterSet):

    order = filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('base_price', 'price'),
        ),
        field_labels={
            'title': _('title (A-Z)'),
            '-title': _('title (Z-A)'),
            'base_price': _('price (ascending)'),
            '-base_price': _('price (descending)'),
        },
        label=_('Sort by'),
        empty_label=_('By arrival date'),
    )
