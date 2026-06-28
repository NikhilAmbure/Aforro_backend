from rest_framework import serializers
from apps.products.models import Product

class ProductSearchSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    inventory_quantity = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "category",
            "inventory_quantity"
        ]

class ProductSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title"]