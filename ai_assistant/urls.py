from django.urls import path

from . import views


app_name = "ai_assistant"

urlpatterns = [
    path("create-web-call/", views.create_web_call, name="create_web_call"),
    path("webhook/", views.webhook, name="webhook"),
]

