from datetime import date

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from vendors.models import Vendor

from .models import VendorAnalytics
from .serializers import VendorAnalyticsSerializer


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def record_vendor_click(request: Request, vendor_id: int) -> Response:
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(
            {"detail": "Vendor not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    analytics, _ = VendorAnalytics.objects.get_or_create(
        vendor=vendor, date=date.today()
    )
    analytics.clicks += 1
    analytics.save(update_fields=["clicks"])
    serializer = VendorAnalyticsSerializer(analytics)
    return Response(serializer.data)

