from django.contrib import admin

from .models import VendorAnalytics


@admin.register(VendorAnalytics)
class VendorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("vendor", "date", "views", "clicks")
    list_filter = ("date", "vendor")
    search_fields = ("vendor__name",)

