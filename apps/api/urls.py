from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from apps.emailapp.views import (
    SendEmailView, PasswordTokenCheckAPI,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,)
from apps.accounts.views import UserTokenObtainPairView
from apps.accounts.views import (
    UserViewSet,
    UserRegisterView,
    UserMeView,
    GroupViewSet,
    PermissionViewSet,
)


from .views import APIRootView


app_name = "api"


# Create a custom router by inheriting from DefaultRouter
# class CustomRouter(DefaultRouter):
#     def get_api_root_view(self, api_urls=None):
#         root_view = super().get_api_root_view(api_urls)
#         root_view.cls.__doc__ = "Your custom API root description here."
#         return root_view


# router = CustomRouter()
router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"permissions", PermissionViewSet)

urlpatterns = [
    path("", APIRootView.as_view(), name="api-root-view"),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        "auth/signin/", UserTokenObtainPairView.as_view(), name="auth-signin"
    ),
    path("auth/register/", UserRegisterView.as_view(), name="auth-register"),
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    # path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('send-email/', SendEmailView.as_view(), name='send-email'),
    path(
        "request-reset-email/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
]

urlpatterns += router.urls
