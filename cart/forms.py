from django import forms


class CartAddForm(forms.Form):

    quantity = forms.IntegerField(
        initial=1,
        widget=forms.TextInput,
    )
    next = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )


class CartRemoveForm(forms.Form):

    next = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
