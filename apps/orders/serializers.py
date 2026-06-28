from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product
from apps.stores.models import Store

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source = "product.title",
        read_only=True
    )
    class Meta:
        model = OrderItem
        fields = ["product", "product_title", "quantity_requested"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "store",
            "status",
            "created_at",
            "items"
        ]

# Input Serializer
class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product"
    )
    quantity_requested = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(),
        source="store"
    )
    items = OrderItemCreateSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError(
                "At least one item is required."
            )
        return value


# Order Listing
class OrderListSerializer(serializers.ModelSerializer):
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "total_items"]
    