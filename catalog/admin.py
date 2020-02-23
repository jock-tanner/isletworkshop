from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin, OrderedTabularInline,
)
from sorl.thumbnail.admin import AdminInlineImageMixin

from .models import Image, Product


class ImageInline(AdminInlineImageMixin, OrderedTabularInline):

    model = Image
    fields = ('move_up_down_links', 'image')
    readonly_fields = ('move_up_down_links', )
    ordering = ('order', )
    extra = 0


class ProductAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):

    inlines = (ImageInline, )


admin.site.register(Product, ProductAdmin)
