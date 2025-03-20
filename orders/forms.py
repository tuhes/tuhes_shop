from django import forms
from orders.models import Order


class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'phone']