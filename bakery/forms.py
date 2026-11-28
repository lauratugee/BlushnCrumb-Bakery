from django import forms
from django.forms import inlineformset_factory
from .models import Product, Order, OrderItem


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields='__all__'

class OrderForm(forms.ModelForm):
    delivery_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Enter your delivery address"}),
    )

    class Meta:
        model=Order
        fields=['order_type', 'delivery_address']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('order_type') == 'delivery' and not cleaned_data.get('delivery_address', '').strip():
            self.add_error('delivery_address', 'Enter a delivery address for delivery orders.')
        if cleaned_data.get('order_type') == 'collection':
            cleaned_data['delivery_address'] = ''
        return cleaned_data


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(stock__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        if product and quantity and quantity > product.stock:
            self.add_error('quantity', f'Only {product.stock} currently in stock.')
        return cleaned_data


class BaseOrderItemFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        quantities = {}
        products = {}
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue
            product = form.cleaned_data.get('product')
            quantity = form.cleaned_data.get('quantity')
            if product and quantity:
                quantities[product.pk] = quantities.get(product.pk, 0) + quantity
                products[product.pk] = product
        for product_id, quantity in quantities.items():
            product = products[product_id]
            if quantity > product.stock:
                raise forms.ValidationError(f"Your total quantity of {product.name} exceeds the available stock ({product.stock}).")

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    formset=BaseOrderItemFormSet,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
