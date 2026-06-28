from rest_framework.generics import ListAPIView

from .models import Inventory
from .serializers import InventoryListSerializer

class StoreInventoryListAPIView(ListAPIView):
    serializer_class = InventoryListSerializer

    def get_queryset(self):
        
        return (
            Inventory.objects
            .filter(store_id=self.kwargs["store_id"])
            .select_related("product", "product__category")
            .order_by("product__title")
        )