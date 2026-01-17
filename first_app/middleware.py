from datetime import timedelta
from django.utils import timezone
from .models import Visitor

class VisitorMiddleware:
    """
    Production-ready visitor tracking middleware:
    - Only logs GET requests
    - Ignores static and media requests
    - Handles proxy headers for real IP
    - Prevents multiple logs for same IP within an hour
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Faqat GET requestlarni yozamiz
        if request.method != "GET":
            return response

        # Statik va media URLlarni o'tkazib yuborish
        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            return response

        # Haqiqiy IP olish (proxy/Render uchun)
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            # X-Forwarded-For bo‘lsa birinchi IP olamiz
            ip = ip.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT", "")

        # Takroriy yozuvni oldini olish (oxirgi 1 soat ichida shu IP yozilmagan bo‘lsa)
        one_hour_ago = timezone.now() - timedelta(hours=1)
        recent = Visitor.objects.filter(ip_address=ip, visited_at__gte=one_hour_ago).exists()

        if not recent:
            Visitor.objects.create(ip_address=ip, user_agent=user_agent)

        return response
