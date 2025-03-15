from django.db import models


class ProductSnapshot(models.Model):
    product_id = models.UUIDField()
    version = models.PositiveIntegerField()

    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
