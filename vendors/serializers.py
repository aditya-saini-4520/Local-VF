from rest_framework import serializers

from .models import Category, Service, Vendor, VendorPhoto


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class VendorPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPhoto
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    photos = VendorPhotoSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    average_rating = serializers.SerializerMethodField()
    is_open_now = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            "id",
            "name",
            "owner",
            "category",
            "category_id",
            "description",
            "address",
            "latitude",
            "longitude",
            "phone",
            "email",
            "website",
            "working_hours",
            "is_open",
            "is_verified",
            "created_at",
            "photos",
            "services",
            "average_rating",
            "is_open_now",
        ]
        read_only_fields = ("owner", "created_at", "is_verified")

    def get_average_rating(self, obj):
        from django.db.models import Avg

        result = obj.reviews.aggregate(avg=Avg("rating"))
        return result["avg"]

    def get_is_open_now(self, obj):
        return obj.is_open_now

