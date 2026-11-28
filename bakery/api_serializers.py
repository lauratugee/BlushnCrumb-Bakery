from collections import defaultdict

from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'product_type', 'product_type_display')


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    order_type = serializers.ChoiceField(choices=Order.DELIVERY_CHOICES)
    delivery_address = serializers.CharField(required=False, allow_blank=True, max_length=500)
    items = OrderItemInputSerializer(many=True, allow_empty=False)

    def validate(self, attrs):
        if attrs['order_type'] == 'delivery' and not attrs.get('delivery_address', '').strip():
            raise serializers.ValidationError({'delivery_address': 'An address is required for delivery.'})
        if attrs['order_type'] == 'collection':
            attrs['delivery_address'] = ''

        requested = defaultdict(int)
        for item in attrs['items']:
            requested[item['product_id']] += item['quantity']
        products = Product.objects.filter(pk__in=requested)
        found = {product.pk: product for product in products}
        errors = {}
        for product_id, quantity in requested.items():
            product = found.get(product_id)
            if product is None:
                errors[str(product_id)] = 'Product not found.'
            elif quantity > product.stock:
                errors[str(product_id)] = f'Only {product.stock} currently in stock for {product.name}.'
        if errors:
            raise serializers.ValidationError({'items': errors})
        attrs['_products'] = found
        attrs['_requested'] = dict(requested)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        products = validated_data.pop('_products')
        requested = validated_data.pop('_requested')
        item_data = validated_data.pop('items')
        order = Order.objects.create(customer=self.context['request'].user, **validated_data)

        for product_id, quantity in requested.items():
            updated = Product.objects.filter(pk=product_id, stock__gte=quantity).update(stock=F('stock') - quantity)
            if not updated:
                raise serializers.ValidationError({'items': f'Not enough stock for {products[product_id].name}.'})

        for item in item_data:
            product = products[item['product_id']]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price,
            )
        return order


class OrderReadSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    order_type_display = serializers.CharField(source='get_order_type_display', read_only=True)
    items = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_date', 'status', 'status_display', 'order_type', 'order_type_display', 'delivery_address', 'items', 'total')

    def get_items(self, order):
        return [
            {
                'product_id': item.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'unit_price': item.price,
                'line_total': item.get_total(),
            }
            for item in order.items.all()
        ]
