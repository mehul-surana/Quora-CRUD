# core/middleware.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        access_token = request.COOKIES.get("access")
        if access_token:
            try:
                validated_token = self.jwt_auth.get_validated_token(access_token)
                user = self.jwt_auth.get_user(validated_token)
                request.user = user
            except Exception:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        return self.get_response(request)
