from datetime import time

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_vendors",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="vendors"
    )
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    working_hours = models.JSONField(default=dict, blank=True)
    is_open = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("vendors:vendor_detail_page", args=[self.pk])

    @property
    def is_open_now(self) -> bool:
        """Determine if vendor is open based on working_hours and current time."""
        if not self.working_hours:
            return self.is_open

        now = timezone.localtime()
        day_key = now.strftime("%a")
        info = self.working_hours.get(day_key)
        if not info:
            return False

        open_str = info.get("open")
        close_str = info.get("close")
        if not open_str or not close_str:
            return False

        try:
            open_time = time.fromisoformat(open_str)
            close_time = time.fromisoformat(close_str)
        except ValueError:
            return False

        current_time = now.time()
        if open_time <= close_time:
            return open_time <= current_time <= close_time
        return current_time >= open_time or current_time <= close_time


class VendorPhoto(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="vendor_photos/")
    is_primary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Photo for {self.vendor.name}"


class Service(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="services"
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.vendor.name})"


class Favourite(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="favourited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("customer", "vendor")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.customer} → {self.vendor}"

