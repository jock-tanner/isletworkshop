from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, activate, gettext_lazy as _,
)


def switch_language(sender, user, request, **kwargs):
    activate(user.language)
    request.session[LANGUAGE_SESSION_KEY] = user.language


class UserConfig(AppConfig):
    name = 'users'
    verbose_name = _('Users')

    def ready(self):
        user_logged_in.connect(switch_language)
