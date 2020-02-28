from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.utils.translation import LANGUAGE_SESSION_KEY, activate
from django.views.generic import View


User = get_user_model()


class SetLanguageView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        language = request.GET.get('lang')
        if language in User.languages:
            request.user.set_language(language)
            activate(language)
            request.session[LANGUAGE_SESSION_KEY] = language

        return HttpResponseRedirect(request.GET.get('next'))
