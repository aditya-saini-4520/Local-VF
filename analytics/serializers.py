from rest_framework import serializers

from .models import VendorAnalytics


class VendorAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAnalytics
        fields = ["id", "vendor", "views", "clicks", "date"]

