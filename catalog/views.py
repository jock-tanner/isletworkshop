from django.views.generic import DetailView
from django_filters.views import FilterView

from .filters import ProductFilterSet
from .models import Product


class CatalogView(FilterView):
    filterset_class = ProductFilterSet
    paginate_by = 6
    paginate_orphans = 3
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'product'


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    pk_url_kwarg = 'product_id'
    context_object_name = 'product'
