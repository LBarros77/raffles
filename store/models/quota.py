from django.db import models
from product.models import Product


class AwardedQuota(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	number = models.PositiveIntegerField(default=0)
