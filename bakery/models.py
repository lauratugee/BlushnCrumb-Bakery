from django.db import models

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
