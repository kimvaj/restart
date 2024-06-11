from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "auth": {
                "signin": reverse("api:auth-signin", request=request),
                "register": reverse("api:auth-register", request=request),
                # 'logout': reverse('api:logout', request=request, format=format),
                # 'password_change': reverse('api:password_change', request=request, format=format),
                "refresh_token": reverse("api:token_refresh", request=request),
                "auth-me": reverse(
                    "api:auth-me", request=request, format=None
                ),
            },
            "users": reverse("api:user-list", request=request, format=None),
            "groups": reverse("api:group-list", request=request, format=None),
            "permissions": reverse(
                "api:permission-list", request=request, format=None
            ),
        }

        return Response(data)
