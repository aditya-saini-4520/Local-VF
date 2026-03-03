from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from vendors.models import Vendor

from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        vendor_id = self.kwargs.get("vendor_id")
        return Review.objects.filter(vendor_id=vendor_id)

    def perform_create(self, serializer):
        vendor_id = self.kwargs.get("vendor_id")
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer.save(customer=self.request.user, vendor=vendor)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def vendor_average_rating(request: Request, vendor_id: int) -> Response:
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    average = Review.average_rating_for_vendor(vendor)
    return Response({"vendor_id": vendor.id, "average_rating": average})

