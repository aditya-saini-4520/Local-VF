from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    customer_username = serializers.ReadOnlyField(source="customer.username")

    class Meta:
        model = Review
        fields = [
            "id",
            "vendor",
            "customer",
            "customer_username",
            "rating",
            "comment",
            "photo",
            "created_at",
        ]
        read_only_fields = ("customer", "created_at")

