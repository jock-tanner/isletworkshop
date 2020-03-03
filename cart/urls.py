from django.urls import path

from .views import CartAddView, CartRemoveView, CartView


app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='list'),
    path('add/<int:product_id>/', CartAddView.as_view(), name='add'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='remove'),
]
