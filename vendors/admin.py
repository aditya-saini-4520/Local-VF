from django.contrib import admin

from .models import Category, Service, Vendor, VendorPhoto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    search_fields = ("name", "slug")


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "category",
        "is_open",
        "is_verified",
        "created_at",
    )
    list_filter = ("is_open", "is_verified", "category")
    search_fields = ("name", "owner__username", "address", "phone", "email")


@admin.register(VendorPhoto)
class VendorPhotoAdmin(admin.ModelAdmin):
    list_display = ("vendor", "is_primary")
    list_filter = ("is_primary",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor", "price")
    search_fields = ("name", "vendor__name")

