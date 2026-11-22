from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Product

class ProductApiTests(TestCase):
    def setUp(self):
        Product.objects.create(name="Test Mouse", category="Electronics", price=500,
                               rating=4.5, review_count=20)
        self.client = APIClient()

    def test_product_list_endpoint(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_summary_endpoint(self):
        response = self.client.get("/api/analytics/summary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_products"], 1)
