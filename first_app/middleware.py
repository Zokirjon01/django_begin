from .models import Visitor

class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        Visitor.objects.create(ip_address=ip, user_agent=user_agent)

        response = self.get_response(request)
        return response
