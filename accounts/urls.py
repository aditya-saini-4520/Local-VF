from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect_view, name="dashboard"),
    path(
        "dashboard/customer/",
        views.customer_dashboard_view,
        name="customer_dashboard",
    ),
    path(
        "dashboard/vendor/",
        views.vendor_dashboard_view,
        name="vendor_dashboard",
    ),
    path("update-profile/", views.update_profile, name="update_profile"),
]

