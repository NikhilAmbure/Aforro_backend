from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from .serializers import OrderCreateSerializer, OrderSerializer, OrderListSerializer
from .services import create_order

from django.db.models import Count
from .models import Order

from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Create a new order",
    description="Creates an order and automatically confirms or rejects it based on inventory availability.",
)
class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = create_order(serializer.validated_data)

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )

class StoreOrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        
        return (
            Order.objects
            .filter(store_id=store_id)
            .annotate(total_items=Count("items"))
            .order_by("-created_at")
        )