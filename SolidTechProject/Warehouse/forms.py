from django import forms

from Warehouse.models import IncomingProduct


class IncomingProductForm(forms.ModelForm):
    class Meta:
        model = IncomingProduct
        fields = ["product","quantity"]