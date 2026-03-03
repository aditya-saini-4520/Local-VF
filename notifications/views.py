from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime

from .models import Notification
from .serializers import NotificationSerializer


class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request: Request, pk: int) -> Response:
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response(
            {"detail": "Notification not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    notification.is_read = True
    notification.save(update_fields=["is_read"])
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request: Request) -> Response:
    """
    Mark all unread notifications as read for the authenticated user.
    """
    unread_count = Notification.objects.filter(
        user=request.user, is_read=False
    ).update(is_read=True)
    
    return Response({
        "detail": f"{unread_count} notification(s) marked as read.",
        "marked_count": unread_count
    }, status=status.HTTP_200_OK)


@login_required
def notifications_api(request):
    """Get all recent notifications for the user"""
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    def time_ago(dt):
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        diff = now - dt
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "just now"
    
    return JsonResponse({
        'notifications': [{
            'id': n.id,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': time_ago(n.created_at),
            'icon': '📢'  # You can add icon field to model later
        } for n in notifs],
        'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()
    })


@login_required
def notification_list(request):
    """Display all notifications for the logged-in user"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })