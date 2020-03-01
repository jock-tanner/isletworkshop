from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('catalog/', include('catalog.urls')),
    path('cart/', include('cart.urls')),
]

if settings.DEBUG:
    urlpatterns.append(
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT},
        )
    )
