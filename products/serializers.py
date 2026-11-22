from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "price", "rating", "review_count",
                  "product_url", "source", "collected_at"]
        read_only_fields = ["id", "collected_at"]

    def validate_rating(self, value):
        if value is not None and not 0 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
