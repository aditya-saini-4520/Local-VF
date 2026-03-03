import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from retell import Retell


client = Retell(api_key=settings.RETELL_API_KEY) if getattr(settings, "RETELL_API_KEY", None) else None


@require_POST
def create_web_call(request: HttpRequest) -> HttpResponse:
    if client is None or not settings.RETELL_AGENT_ID:
        return JsonResponse(
            {"detail": "Voice assistant is not configured."}, status=503
        )

    try:
        payload = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        payload = {}

    search_context = payload.get("search_context") or ""
    user_location = payload.get("location") or ""

    dynamic_vars = {
        "user_location": user_location,
        "search_context": search_context,
    }
    if request.user.is_authenticated:
        dynamic_vars["user_id"] = str(request.user.id)

    web_call = client.call.create_web_call(
        agent_id=settings.RETELL_AGENT_ID,
        retell_llm_dynamic_variables=dynamic_vars,
    )

    return JsonResponse({"access_token": web_call.access_token})


@csrf_exempt
@require_POST
def webhook(request: HttpRequest) -> HttpResponse:
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        data = {}

    event_type = data.get("event_type")
    if event_type == "call_ended":
        # Retell will send transcript or summary fields here; we simply acknowledge.
        # You can extend this to store analytics or logs if desired.
        pass

    return JsonResponse({"status": "ok"})

