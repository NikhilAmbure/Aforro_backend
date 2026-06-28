from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Category, Product


class ProductSuggestionAPITest(APITestCase):

    def setUp(self):
        category = Category.objects.create(
            name="Electronics"
        )

        Product.objects.create(
            title="Gaming Laptop",
            description="Gaming Laptop",
            price=50000,
            category=category,
        )

        Product.objects.create(
            title="Laptop Stand",
            description="Laptop Stand",
            price=2000,
            category=category,
        )

    def test_product_suggestions(self):

        response = self.client.get(
            "/api/search/suggest/?q=lap"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertLessEqual(
            len(response.data),
            10,
        )

        titles = [item["title"] for item in response.data]

        self.assertIn(
            "Gaming Laptop",
            titles,
        )

        self.assertIn(
            "Laptop Stand",
            titles,
        )
