from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Category, Product
from apps.stores.models import Store, Inventory
from apps.orders.models import Order


class OrderAPITest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics"
        )

        self.product = Product.objects.create(
            title="Laptop",
            description="Gaming Laptop",
            price=50000,
            category=self.category,
        )

        self.store = Store.objects.create(
            name="Main Store",
            location="Pune",
        )

        Inventory.objects.create(
            store=self.store,
            product=self.product,
            quantity=20,
        )

    def test_create_confirmed_order(self):

        payload = {
            "store_id": self.store.id,
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity_requested": 5,
                }
            ],
        }

        response = self.client.post(
            "/api/orders/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["status"],
            Order.StatusChoices.CONFIRMED,
        )

    def test_create_rejected_order(self):

        payload = {
            "store_id": self.store.id,
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity_requested": 100,
                }
            ],
        }

        response = self.client.post(
            "/api/orders/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["status"],
            Order.StatusChoices.REJECTED,
        )