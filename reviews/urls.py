from django.urls import path

from . import views


app_name = "reviews"

urlpatterns = [
    path(
        "vendor/<int:vendor_id>/",
        views.ReviewListCreateView.as_view(),
        name="vendor_reviews",
    ),
    path(
        "vendor/<int:vendor_id>/average/",
        views.vendor_average_rating,
        name="vendor_average_rating",
    ),
]

