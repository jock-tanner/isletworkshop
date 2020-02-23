from django.views.generic import DetailView, ListView

from .models import Product


class CatalogView(ListView):
    paginate_by = 12
    paginate_orphans = 3
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'product'


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    pk_url_kwarg = 'product_id'
    context_object_name = 'product'
