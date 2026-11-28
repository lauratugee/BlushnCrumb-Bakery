from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    PRODUCT_TYPES = [
        ('ready_made', 'Ready made'),
        ('custom_made', 'Custom made'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    product_type = models.CharField(
        choices=PRODUCT_TYPES,
        max_length=20,
    default='ready_made'
    )

    def __str__(self):
        return self.name

class Order(models.Model):

    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('canceled', 'Canceled'),
    ]
    DELIVERY_CHOICES = [
        ('delivery', 'Delivery'),
        ('collection', 'Collection'),
    ]
    order_type= models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default='collection',
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    order_date = models.DateField(auto_now_add=True)

    status=models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='pending'
    )
    delivery_address=models.TextField(blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)

    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f" {self.quantity} x {self.product.name}"

    def get_total(self):
        return self.price * self.quantity
