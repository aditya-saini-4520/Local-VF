import math
from datetime import date

from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from analytics.models import VendorAnalytics
from reviews.models import Review

from .models import Category, Favourite, Service, Vendor, VendorPhoto
from .serializers import VendorSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)


@method_decorator(login_required, name="dispatch")
class VendorCreateView(generics.CreateAPIView):
    serializer_class = VendorSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            Vendor.objects.select_related("category")
            .annotate(avg_rating=Avg("reviews__rating"))
            .all()
        )
        search = self.request.query_params.get("search")
        category = self.request.query_params.get("category")
        is_open = self.request.query_params.get("is_open")
        min_rating = self.request.query_params.get("min_rating")

        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(address__icontains=search)
                | Q(description__icontains=search)
            )
        if category:
            qs = qs.filter(category_id=category)
        if is_open == "1":
            qs = qs.filter(is_open=True)
        if min_rating:
            try:
                value = float(min_rating)
            except ValueError:
                value = None
            if value is not None:
                qs = qs.filter(avg_rating__gte=value)
        return qs


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request: Request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        vendor: Vendor = self.get_object()
        analytics, _ = VendorAnalytics.objects.get_or_create(
            vendor=vendor, date=date.today()
        )
        analytics.views += 1
        analytics.save(update_fields=["views"])
        return response


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def toggle_vendor_open_status(request: Request, pk: int) -> Response:
    try:
        vendor = Vendor.objects.get(pk=pk, owner=request.user)
    except Vendor.DoesNotExist:
        return Response(
            {"detail": "Vendor not found or permission denied."},
            status=status.HTTP_404_NOT_FOUND,
        )

    vendor.is_open = not vendor.is_open
    vendor.save(update_fields=["is_open"])
    return Response({"id": vendor.id, "is_open": vendor.is_open})


def _haversine_distance_km(lat1, lon1, lat2, lon2) -> float:
    r = 6371.0
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(
        dlambda / 2
    ) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def nearby_vendors(request: Request) -> Response:
    try:
        lat = float(request.query_params.get("lat", ""))
        lon = float(request.query_params.get("lon", ""))
        radius_km = float(request.query_params.get("radius", "5"))
    except ValueError:
        return Response(
            {"detail": "lat, lon must be valid numbers."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    vendors = Vendor.objects.exclude(latitude__isnull=True).exclude(
        longitude__isnull=True
    )
    results = []
    for vendor in vendors:
        distance = _haversine_distance_km(
            lat, lon, vendor.latitude, vendor.longitude
        )
        if distance <= radius_km:
            data = VendorSerializer(vendor).data
            data["distance_km"] = round(distance, 2)
            results.append(data)

    return Response(results)


def vendor_list_page(request: HttpRequest):
    categories = Category.objects.all()
    favourite_ids: list[int] = []
    if request.user.is_authenticated:
        favourite_ids = list(
            Favourite.objects.filter(customer=request.user).values_list(
                "vendor_id", flat=True
            )
        )
    return render(
        request,
        "vendors/vendor_list.html",
        {
            "categories": categories,
            "favourite_ids": favourite_ids,
        },
    )


def vendor_detail_page(request: HttpRequest, pk: int):
    vendor = get_object_or_404(
        Vendor.objects.select_related("category").prefetch_related("photos", "services"),
        pk=pk,
    )
    
    # Track recently viewed vendors (last 5)
    recently_viewed = request.session.get("recently_viewed", [])
    if pk not in recently_viewed:
        recently_viewed = [pk] + recently_viewed[:4]
        request.session["recently_viewed"] = recently_viewed
    
    # Get people also viewed (3 vendors from same category, excluding current)
    people_also_viewed = []
    if vendor.category:
        people_also_viewed = (
            Vendor.objects.filter(category=vendor.category)
            .exclude(pk=pk)
            .select_related("category")[:3]
        )
    
    reviews = Review.objects.filter(vendor=vendor).select_related("customer").prefetch_related("photos")
    average = reviews.aggregate(avg=Avg("rating"))["avg"]
    
    # Get review count by rating
    rating_breakdown = {}
    for i in range(5, 0, -1):
        rating_breakdown[i] = reviews.filter(rating=i).count()
    
    # Check if user has favourited this vendor
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(
            customer=request.user, vendor=vendor
        ).exists()
    
    today_index = date.today().weekday()
    return render(
        request,
        "vendors/vendor_detail.html",
        {
            "vendor": vendor,
            "photos": vendor.photos.all(),
            "services": vendor.services.all(),
            "reviews": reviews,
            "average_rating": average,
            "rating_breakdown": rating_breakdown,
            "today_index": today_index,
            "people_also_viewed": people_also_viewed,
            "is_favourite": is_favourite,
        },
    )


@login_required
def vendor_register(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        description = request.POST.get("description", "")
        address = request.POST.get("address", "")
        latitude = request.POST.get("latitude") or None
        longitude = request.POST.get("longitude") or None
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        website = request.POST.get("website", "")
        working_hours_json = request.POST.get("working_hours") or "{}"
        from json import loads

        try:
            working_hours = loads(working_hours_json)
        except Exception:
            working_hours = {}

        errors = []
        if not name:
            errors.append("Name is required.")
        if not address:
            errors.append("Address is required.")

        if errors:
            categories = Category.objects.all()
            return render(
                request,
                "vendors/vendor_register.html",
                {"categories": categories, "errors": errors},
            )

        category = Category.objects.filter(pk=category_id).first() if category_id else None
        vendor = Vendor.objects.create(
            name=name,
            owner=request.user,
            category=category,
            description=description,
            address=address,
            latitude=latitude,
            longitude=longitude,
            phone=phone,
            email=email,
            website=website,
            working_hours=working_hours,
        )
        for image in request.FILES.getlist("photos"):
            VendorPhoto.objects.create(vendor=vendor, image=image)
        return redirect(f"{request.path}?success=1")

    categories = Category.objects.all()
    return render(
        request,
        "vendors/vendor_register.html",
        {"categories": categories},
    )


@login_required
@login_required
def vendor_dashboard_page(request: HttpRequest):
    vendor = (
        Vendor.objects.filter(owner=request.user)
        .prefetch_related("services", "reviews")
        .first()
    )
    from django.db.models import Sum
    from django.utils import timezone
    from datetime import timedelta

    views = clicks = avg_rating = review_count = 0
    recent_reviews = []
    seven_day_analytics = {}
    
    if vendor:
        analytics = vendor.analytics.aggregate(
            total_views=Sum("views"), total_clicks=Sum("clicks")
        )
        views = analytics["total_views"] or 0
        clicks = analytics["total_clicks"] or 0
        review_stats = vendor.reviews.aggregate(avg=Avg("rating"))
        avg_rating = review_stats["avg"] or 0
        review_count = vendor.reviews.count()
        recent_reviews = vendor.reviews.select_related("customer")[:5]
        
        # Get 7-day analytics
        today = timezone.now().date()
        for i in range(6, -1, -1):
            date_key = today - timedelta(days=i)
            day_views = (
                vendor.analytics.filter(date=date_key).aggregate(
                    total=Sum("views")
                )["total"]
                or 0
            )
            seven_day_analytics[date_key.strftime("%a")] = day_views

    # Calculate profile completion
    profile_complete = 0
    total_fields = 6
    if vendor:
        if vendor.name:
            profile_complete += 1
        if vendor.address:
            profile_complete += 1
        if vendor.phone:
            profile_complete += 1
        if vendor.photos.exists():
            profile_complete += 1
        if vendor.working_hours:
            profile_complete += 1
        if vendor.services.exists():
            profile_complete += 1
    
    profile_completion_percent = int((profile_complete / total_fields) * 100) if total_fields else 0

    return render(
        request,
        "vendors/vendor_dashboard.html",
        {
            "vendor": vendor,
            "views_count": views,
            "clicks_count": clicks,
            "average_rating": avg_rating,
            "review_count": review_count,
            "services": vendor.services.all() if vendor else [],
            "recent_reviews": recent_reviews,
            "vendor_profile_url": vendor.get_absolute_url() if vendor else "",
            "seven_day_analytics": seven_day_analytics,
            "profile_complete": profile_complete,
            "profile_completion_percent": profile_completion_percent,
        },
    )


@login_required
def toggle_favourite(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed."}, status=405)

    vendor = get_object_or_404(Vendor, pk=pk)
    favourite, created = Favourite.objects.get_or_create(
        customer=request.user, vendor=vendor
    )
    if not created:
        favourite.delete()
        is_favourite = False
    else:
        is_favourite = True

    return JsonResponse({"is_favourite": is_favourite})


def vendor_qr(request: HttpRequest, pk: int) -> HttpResponse:
    import qrcode

    vendor = get_object_or_404(Vendor, pk=pk)
    target_url = request.build_absolute_uri(vendor.get_absolute_url())
    img = qrcode.make(target_url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type="image/png")


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def vendor_search_api(request: Request) -> Response:
    qs = (
        Vendor.objects.select_related("category")
        .annotate(avg_rating=Avg("reviews__rating"))
        .all()
    )
    q = request.query_params.get("q")
    category = request.query_params.get("category")
    is_open = request.query_params.get("is_open")
    min_rating = request.query_params.get("min_rating")
    lat = request.query_params.get("lat")
    lon = request.query_params.get("lon")
    radius = request.query_params.get("radius")

    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(address__icontains=q)
            | Q(description__icontains=q)
        )
    if category:
        qs = qs.filter(category_id=category)
    if is_open == "1":
        qs = [v for v in qs if v.is_open_now]
    if min_rating:
        try:
            value = float(min_rating)
        except ValueError:
            value = None
        if value is not None:
            qs = [v for v in qs if (getattr(v, "avg_rating", 0) or 0) >= value]

    results = []
    lat_val = lon_val = radius_val = None
    if lat and lon and radius:
        try:
            lat_val = float(lat)
            lon_val = float(lon)
            radius_val = float(radius)
        except ValueError:
            lat_val = lon_val = radius_val = None

    for vendor in qs:
        distance = None
        if lat_val is not None and vendor.latitude and vendor.longitude:
            distance = _haversine_distance_km(
                lat_val, lon_val, vendor.latitude, vendor.longitude
            )
            if radius_val is not None and distance > radius_val:
                continue
        data = VendorSerializer(vendor).data
        if distance is not None:
            data["distance_km"] = round(distance, 2)
        results.append((vendor.is_verified, distance or 0, data))

    results.sort(key=lambda item: (not item[0], item[1]))

    return Response([item[2] for item in results])

