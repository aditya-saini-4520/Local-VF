from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("vendor", "customer", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("vendor__name", "customer__username", "comment")

