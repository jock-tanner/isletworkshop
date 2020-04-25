from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import LANGUAGE_SESSION_KEY, activate
from django.views.generic import (
    CreateView, DeleteView, UpdateView, ListView, View,
)

from .models import Address


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


class AddressListView(ListView):
    model = Address
    template_name = 'users/address_list.html'
    context_object_name = 'addresses'
    paginate_by = 12
    paginate_orphans = 2
    page_kwarg = 'p'

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user,
        ).order_by('-created_at')


class AddressUpdateView(UpdateView):
    model = Address
    template_name = 'users/address_update.html'
    context_object_name = 'address'
    pk_url_kwarg = 'address_id'
    fields = (
        'postal_code', 'country', 'region',
        'city', 'street', 'building', 'flat',
    )

    def get_success_url(self):
        return reverse(
            'users:address_update',
            kwargs={'address_id': self.object.id},
        )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class AddressCreateView(CreateView):
    model = Address
    template_name = 'users/address_update.html'
    pk_url_kwarg = 'address_id'
    fields = (
        'postal_code', 'country', 'region',
        'city', 'street', 'building', 'flat',
    )
    create_view = True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            'users:address_update',
            kwargs={'address_id': self.object.id},
        )


class AddressDeleteView(DeleteView):
    model = Address
    pk_url_kwarg = 'address_id'
    success_url = reverse_lazy('users:address_list')
