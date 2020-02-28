from django.urls import path

from .views import SetLanguageView


app_name = 'users'

urlpatterns = [
    path('language/', SetLanguageView.as_view(), name='language'),
]
