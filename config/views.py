from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Avg

from accounts.models import UserProfile
from vendors.models import Vendor, Category
from reviews.models import Review


def custom_404(request, exception, template_name="404.html"):
    return render(request, template_name, status=404)


def custom_500(request, template_name="500.html"):
    return render(request, template_name, status=500)


def home(request):
    # Get trending vendors ordered by average rating
    trending_vendors = (
        Vendor.objects.select_related("category")
        .annotate(avg_rating=Avg("reviews__rating"))
        .order_by("-avg_rating")[:6]
    )
    
    # Get recently added vendors
    recently_added = Vendor.objects.select_related("category").order_by("-created_at")[:4]
    
    # Get all categories for featured grid
    categories = Category.objects.all()
    
    # Get real stats
    total_vendors = Vendor.objects.count()
    total_customers = UserProfile.objects.filter(role=UserProfile.Roles.CUSTOMER).count()
    total_cities = (
        Vendor.objects.exclude(address="")
        .values_list("address", flat=True)
        .distinct()
        .count()
    )
    
    # Hardcoded testimonials
    testimonials = [
        {
            "name": "Sarah Johnson",
            "initials": "SJ",
            "rating": 5,
            "text": "Amazing platform! Found a reliable plumber in minutes. Professional, affordable, and quick service. Highly recommended!",
        },
        {
            "name": "Rajesh Kumar",
            "initials": "RK",
            "rating": 5,
            "text": "The vendor verification process is so trustworthy. I bookmarked 5 vendors and each one delivered exceptional service.",
        },
        {
            "name": "Emma Wilson",
            "initials": "EW",
            "rating": 5,
            "text": "Local VFC saved me hours of searching. The reviews are genuine and the ratings accurate. Will use again for sure!",
        },
    ]
    
    context = {
        "trending_vendors": trending_vendors,
        "recently_added": recently_added,
        "categories": categories,
        "total_vendors": total_vendors,
        "total_customers": total_customers,
        "total_cities": total_cities,
        "total_reviews": Review.objects.count(),
        "testimonials": testimonials,
    }
    return render(request, "home.html", context)

