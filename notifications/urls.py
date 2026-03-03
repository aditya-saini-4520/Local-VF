from django.urls import path

from . import views


app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="notification_list"),
    path("unread/", views.UnreadNotificationListView.as_view(), name="unread_notifications"),
    path("<int:pk>/read/", views.mark_notification_read, name="mark_notification_read"),
    path("read-all/", views.mark_all_notifications_read, name="mark_all_read"),
    path("api/", views.notifications_api, name="notifications_api"),
]