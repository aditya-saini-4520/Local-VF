from django.urls import path

from . import views


app_name = "vendors"

urlpatterns = [
    # HTML pages
    path("browse/", views.vendor_list_page, name="vendor_list_page"),
    path("<int:pk>/detail/", views.vendor_detail_page, name="vendor_detail_page"),
    path("register/", views.vendor_register, name="vendor_register"),
    path("dashboard/", views.vendor_dashboard_page, name="vendor_dashboard_page"),
    # JSON APIs
    path("", views.VendorListView.as_view(), name="vendor_list"),
    path("create/", views.VendorCreateView.as_view(), name="vendor_create"),
    path("<int:pk>/", views.VendorDetailView.as_view(), name="vendor_detail"),
    path(
        "<int:pk>/toggle-open/",
        views.toggle_vendor_open_status,
        name="vendor_toggle_open",
    ),
    path("<int:pk>/favourite/", views.toggle_favourite, name="vendor_favourite"),
    path("<int:pk>/qr/", views.vendor_qr, name="vendor_qr"),
    path("api/search/", views.vendor_search_api, name="vendor_search_api"),
    path("nearby/", views.nearby_vendors, name="nearby_vendors"),
]

