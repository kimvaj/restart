from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse

class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "auth": {
                "signin": self.request.build_absolute_uri(reverse("api:auth-signin")),
                "register": self.request.build_absolute_uri(reverse("api:auth-register")),
                "refresh_token": self.request.build_absolute_uri(reverse("api:token_refresh")),
                # Assuming you have an endpoint for 'auth-me'
                # "auth-me": self.request.build_absolute_uri(reverse("api:auth-me")),
            },
            "users": self.request.build_absolute_uri(reverse("api:user-list")),
            "groups": self.request.build_absolute_uri(reverse("api:group-list")),
            "permissions": self.request.build_absolute_uri(reverse("api:permission-list")),
            "send_email": self.request.build_absolute_uri(reverse("api:send-email")),
            "request_reset_email": self.request.build_absolute_uri(reverse("api:request-reset-email")),
            "password_reset_confirm": self.request.build_absolute_uri(reverse("api:password-reset-confirm", kwargs={'uidb64': '<uidb64>', 'token': '<token>'})),
            "password_reset_complete": self.request.build_absolute_uri(reverse("api:password-reset-complete")),
        }
        return Response(data)



# 'logout': reverse('api:logout', request=request, format=format),
                # 'password_change': reverse('api:password_change', request=request, format=format),
                