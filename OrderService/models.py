from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from django.conf import settings

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    product_id = models.UUIDField(unique=True, default=uuid4(), editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


# class Order(models.Model):
#     PAYMENT_STATUS_PENDING = 'P'
#     PAYMENT_STATUS_SHIPPED = 'C'
#     PAYMENT_STATUS_ARRIVED = 'F'
#     PAYMENT_STATUS_CHOICES = [
#         (PAYMENT_STATUS_PENDING, 'Pending'),
#         (PAYMENT_STATUS_SHIPPED, 'Shipped'),
#         (PAYMENT_STATUS_ARRIVED, 'Arrived')
#     ]

#     order_id = models.UUIDField(unique=True, default=uuid4(), editable=False)
#     placed_at = models.DateTimeField(auto_now_add=True)
#     payment_status = models.CharField(
#         max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.PROTECT)
#     product = models.ForeignKey(
#         Product, on_delete=models.PROTECT, related_name='orderitems')
#     quantity = models.PositiveSmallIntegerField()
#     unit_price = models.PositiveIntegerField(validators=[MinValueValidator(1)])


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['order', 'product']]