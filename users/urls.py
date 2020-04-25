from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (
    AddressCreateView, AddressDeleteView, AddressListView, AddressUpdateView,
    SetLanguageView,
)


app_name = 'users'

urlpatterns = [
    path('language/', SetLanguageView.as_view(), name='language'),
    path(
        'address/',
        login_required(AddressListView.as_view()),
        name='address_list',
    ),
    path(
        'address/<int:address_id>/',
        login_required(AddressUpdateView.as_view()),
        name='address_update',
    ),
    path(
        'address/new/',
        login_required(AddressCreateView.as_view()),
        name='address_create',
    ),
    path(
        'address/delete/<int:address_id>/',
        login_required(AddressDeleteView.as_view()),
        name='address_delete',
    ),
]
