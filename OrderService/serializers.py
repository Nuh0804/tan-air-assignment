from decimal import Decimal
from .models import *
from rest_framework import serializers
from django.db import transaction


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(0.18)
    

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: OrderItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price']


class AddOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value):
            raise serializers.ValidationError(
                'No product with the given ID is found')
        return value

    def save(self, **kwargs):
        order_id = self.context['order_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            order_item = OrderItem.objects.get(
                order_id=order_id, product_id=product_id)
            order_item.quantity += quantity
            order_item.save()
            self.instance = order_item
        except OrderItem.DoesNotExist:
            self.instance = OrderItem.objects.create(
                order_id=order_id, **self.validated_data)

        return self.instance

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity']


class UpdateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']

