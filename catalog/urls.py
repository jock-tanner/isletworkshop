from django.urls import path

from .views import CatalogView, ProductView


app_name = 'catalog'

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('<int:product_id>/', ProductView.as_view(), name='product'),
]
