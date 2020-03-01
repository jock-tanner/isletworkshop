from django.urls import path

from .views import CartAddView, CartRemoveView


app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', CartAddView.as_view(), name='add'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='remove'),
]
