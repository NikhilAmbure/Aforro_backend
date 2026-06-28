from django.urls import path
from .views import ProductSearchAPIView, ProductSuggestionAPIView

urlpatterns = [
    path("search/products/", ProductSearchAPIView.as_view(), name="product-search",),
    path('search/suggest/', ProductSuggestionAPIView.as_view(), name="product-suggest"),
]