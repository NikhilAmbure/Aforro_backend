from django.db.models import (
    Q,
    Case,
    When,
    Value,
    IntegerField,
    F,
)
from rest_framework.generics import ListAPIView

from apps.products.models import Product
from .serializers import ProductSearchSerializer, ProductSuggestionSerializer
from rest_framework.exceptions import ValidationError


class ProductSearchAPIView(ListAPIView):
    serializer_class = ProductSearchSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category")

        # By keyword
        query = self.request.query_params.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
            ).annotate(
                relevance=Case(
                    When(title__icontains=query, then=Value(3)),
                    When(description__icontains=query, then=Value(2)),
                    When(category__name__icontains=query, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
        
        # Category filter
        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(
                category__name__iexact=category
            )

        # Price filter
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Store filter
        store_id = self.request.query_params.get("store_id")

        if store_id:
            queryset = queryset.filter(
                inventory__store_id=store_id
            ).annotate(
                inventory_quantity=F("inventory__quantity")
            )

        # In stock filter
        in_stock = self.request.query_params.get("in_stock")

        if in_stock and in_stock.lower() == "true":
            queryset = queryset.filter(
                inventory__quantity__gt=0
            )

        # Sorting

        sort = self.request.query_params.get("sort")

        if sort == "price":
            queryset = queryset.order_by("price")

        elif sort == "-price":
            queryset = queryset.order_by("-price")

        elif sort == "newest":
            queryset = queryset.order_by("-id")

        elif sort == "relevance":
            if query:
                queryset = queryset.order_by("-relevance", "title")    

        return queryset.distinct()
    

class ProductSuggestionAPIView(ListAPIView):
    serializer_class = ProductSuggestionSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()

        if len(query) < 3:
            raise ValidationError(
                {"q": "Query must contain at least 3 characters."}
            )

        return (
            Product.objects.filter(
                Q(title__icontains=query)
            )
            .annotate(
                priority=Case(
                    When(title__istartswith=query, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            )
            .order_by("priority", "title")[:10]
        )