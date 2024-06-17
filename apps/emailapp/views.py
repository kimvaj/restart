from .tasks import send_email_task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from django.shortcuts import render
from rest_framework import generics, status
from .serializers import (
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    EmailSerializer
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect

import os

logger = logging.getLogger(__name__)


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get("APP_SCHEME"), "http", "https"]


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        redirect_url = request.data.get("redirect_url", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse(
                "password-reset-confirm",
                kwargs={"uidb64": uidb64, "token": token},
            )
            absurl = f"http://{current_site}{relative_link}"
            email_body = f"Hello, \n Use the link below to reset your password \n{absurl}?redirect_url={redirect_url}"
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your password",
            }
            Util.send_email(data)
            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Email not registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get("APP_SCHEME"), "http", "https"]


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get("redirect_url", "")
        try:
            uidb64_padded = uidb64 + "=" * (
                -len(uidb64) % 4
            )  # Add padding to uidb64 if needed
            id = smart_str(urlsafe_base64_decode(uidb64_padded))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if redirect_url:
                    return CustomRedirect(f"{redirect_url}?token_valid=False")
                return CustomRedirect(
                    f"{os.environ.get('FRONTEND_URL', '')}?token_valid=False"
                )

            if redirect_url:
                return CustomRedirect(
                    f"{redirect_url}?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}"
                )
            return CustomRedirect(
                f"{os.environ.get('FRONTEND_URL', '')}?token_valid=True"
            )

        except DjangoUnicodeDecodeError:
            if redirect_url:
                return CustomRedirect(f"{redirect_url}?token_valid=False")
            return CustomRedirect(
                f"{os.environ.get('FRONTEND_URL', '')}?token_valid=False"
            )
        except ValueError:
            return Response(
                {"error": "Invalid token or uidb64"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )






class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming send_email_task is a celery task or similar
            send_email_task.delay(serializer.validated_data)
            return Response(
                {"message": "Email is being processed."},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

