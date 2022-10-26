from django.forms import ModelForm, Textarea
from .models import *


class PurchaseForm(ModelForm):
    class Meta:
        model = MyCart
        fields = ['quantity_purchased']   