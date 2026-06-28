from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Category, Product
from apps.stores.models import Store, Inventory


class InventoryAPITest(APITestCase):

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
            quantity=25,
        )

    def test_inventory_list(self):

        response = self.client.get(
            f"/api/stores/{self.store.id}/inventory/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        if isinstance(response.data, dict):
            self.assertGreater(
                len(response.data["results"]),
                0,
            )
        else:
            self.assertGreater(
                len(response.data),
                0,
            )
