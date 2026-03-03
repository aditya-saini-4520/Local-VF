from django.urls import path

from . import views


app_name = "analytics"

urlpatterns = [
    path("vendor/<int:vendor_id>/click/", views.record_vendor_click, name="record_vendor_click"),
]

