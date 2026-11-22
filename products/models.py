from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.PositiveIntegerField(default=0)
    product_url = models.URLField(max_length=500, blank=True)
    source = models.CharField(max_length=100, default="sample dataset")
    collected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["category", "price"])]

    def __str__(self):
        return self.name
