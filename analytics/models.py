from django.db import models

from vendors.models import Vendor


class VendorAnalytics(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="analytics"
    )
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    date = models.DateField()

    class Meta:
        unique_together = ("vendor", "date")
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"Analytics for {self.vendor.name} on {self.date}"

