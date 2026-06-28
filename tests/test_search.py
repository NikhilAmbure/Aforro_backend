from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Category, Product


class ProductSearchAPITest(APITestCase):

    def setUp(self):
        category = Category.objects.create(
            name="Electronics"
        )

        Product.objects.create(
            title="Gaming Laptop",
            description="Powerful laptop",
            price=60000,
            category=category,
        )

    def test_search_product(self):

        response = self.client.get(
            "/api/search/products/?q=laptop"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreater(
            response.data["count"],
            0,
        )
