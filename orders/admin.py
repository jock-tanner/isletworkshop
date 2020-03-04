from django.contrib import admin

from .models import Order, OrderLine


class OrderLineInline(admin.StackedInline):
    model = OrderLine
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineInline, )


admin.site.register(Order, OrderAdmin)
