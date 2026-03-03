from django.conf import settings
from django.db import models

from vendors.models import Vendor


class Review(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="reviews"
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    photo = models.ImageField(upload_to="review_photos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Review {self.rating} for {self.vendor.name} by {self.customer}"

    @staticmethod
    def average_rating_for_vendor(vendor: Vendor) -> float | None:
        from django.db.models import Avg

        result = Review.objects.filter(vendor=vendor).aggregate(avg=Avg("rating"))
        return result["avg"]

