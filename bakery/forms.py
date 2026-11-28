from django import forms
from django.forms import inlineformset_factory
from .models import Product, Order, OrderItem


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields='__all__'

class OrderForm(forms.ModelForm):

    class Meta:
        model=Order
        fields=['order_type', 'delivery_address']

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
