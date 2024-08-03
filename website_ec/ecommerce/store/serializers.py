# serializers.py

from rest_framework import serializers
from .models import OrderItem

from .models import Product

from rest_framework import serializers
from .models import OrderItem, Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price= serializers.SerializerMethodField()
    location= serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['product_name','product_price','quantity','location']  # Include 'product_name'

    def get_product_name(self, obj):
        # Return the name of the product related to the OrderItem
        if obj.product:
            return obj.product.name
        return 'Unknown'
    def get_product_price(self, obj):
        # Return the price of the product related to the OrderItem
        if obj.product:
            return obj.product.price
        return 0
    def get_location(self, obj):
        # Return the price of the product related to the OrderItem
        if obj.product:
            return obj.product.location
        return 'unknown'

    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'