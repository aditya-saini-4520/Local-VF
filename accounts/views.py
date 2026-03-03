from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from reviews.models import Review
from vendors.models import Favourite, Vendor

from .models import UserProfile


@require_http_methods(["GET", "POST"])
def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role", "customer")
        
        if password1 != password2:
            return render(request, "accounts/login.html", {"mode": "register", "register_error": "Passwords do not match"})
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/login.html", {"mode": "register", "register_error": "Username already taken"})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.get_or_create(user=user, defaults={"role": role})
        login(request, user)
        return redirect("home")
    
    return render(request, "accounts/login.html", {"mode": "register"})


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get("next") or "home")
        return render(request, "accounts/login.html", {"mode": "login", "login_error": True})
    return render(request, "accounts/login.html", {"mode": "login"})


@require_http_methods(["POST"])
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")


@login_required
@require_GET
def dashboard_redirect_view(request: HttpRequest) -> HttpResponse:
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == UserProfile.Roles.VENDOR:
        return redirect("vendors:vendor_dashboard_page")
    return redirect("accounts:customer_dashboard")


@login_required
@require_GET
def customer_dashboard_view(request: HttpRequest) -> HttpResponse:
    favourite_vendors = Vendor.objects.filter(
        favourited_by__customer=request.user
    ).distinct()[:8]
    recent_reviews = Review.objects.filter(customer=request.user).select_related("vendor")[:5]
    
    # Get recently viewed vendors from session
    recently_viewed_ids = request.session.get("recently_viewed", [])
    recently_viewed = []
    if recently_viewed_ids:
        recently_viewed = Vendor.objects.filter(pk__in=recently_viewed_ids).select_related("category")[:5]
    
    # Get search history from session
    search_history = request.session.get("search_history", [])[:5]
    
    # Profile completion - calculate based on username, email, phone, location, avatar
    profile = getattr(request.user, "profile", None)
    completion_fields = [
        bool(request.user.username),
        bool(request.user.email),
    ]
    if profile:
        completion_fields.extend([
            bool(profile.phone),
            bool(profile.location),
            bool(profile.avatar),
        ])
    
    completion_percent = int((sum(completion_fields) / len(completion_fields)) * 100) if completion_fields else 0
    
    return render(
        request,
        "accounts/customer_dashboard.html",
        {
            "favourite_vendors": favourite_vendors,
            "recent_reviews": recent_reviews,
            "recently_viewed_vendors": recently_viewed,
            "search_history": search_history,
            "profile_completion": completion_percent,
            "user": request.user,
            "profile": profile,
            "username": request.user.username,
            "email": request.user.email,
            "location": profile.location if profile else "",
            "phone": profile.phone if profile else "",
            "avatar": profile.avatar if profile else None,
        },
    )


@login_required
@require_GET
def vendor_dashboard_view(request: HttpRequest) -> HttpResponse:
    return redirect("vendors:vendor_dashboard_page")


@login_required
@require_http_methods(["POST"])
def update_profile(request: HttpRequest) -> HttpResponse:
    """Update user profile via AJAX"""
    try:
        profile = request.user.profile
        
        # Save email on the User model
        new_email = request.POST.get('email', '').strip()
        if new_email and new_email != request.user.email:
            # Check email not already taken by another user
            if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
                return JsonResponse({'success': False, 'message': 'Email already in use'})
            request.user.email = new_email
            request.user.save(update_fields=['email'])
        
        # Update profile fields
        if location := request.POST.get('location'):
            profile.location = location
        if phone := request.POST.get('phone'):
            profile.phone = phone
        if avatar := request.FILES.get('avatar'):
            profile.avatar = avatar
            
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully! ✅'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

