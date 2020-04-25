from django.contrib import admin
from django.contrib.auth.models import Group as OldGroup
from django.contrib.auth.admin import GroupAdmin, UserAdmin as OldUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Address, Group, User


class UserAdmin(OldUserAdmin):

    fieldsets = (
        (None, {'fields': ('password', )}),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name', 'middle_name', 'last_name',
                    'email', 'is_email_verified',
                ),
            },
        ),
        (
            _('Permissions'), {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'groups',
                    'user_permissions',
                ),
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Internationalization'), {'fields': ('language', )}),
    )
    ordering = ('email', )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


admin.site.unregister(OldGroup)

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Address)
