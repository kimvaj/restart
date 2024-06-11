from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group, Permission
from django.http import Http404
from .models import User
from .serializers import (
    GroupSerializer,
    PermissionSerializer,
    UserTokenObtainPairSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from common.viewsets.base_viewsets import BaseModelViewSet


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Retrieve the user from the serializer
            user = serializer.user

            # Add custom claims to the response data
            response.data["user_id"] = user.id
            response.data["email"] = user.email

        return response


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


class UserMeView(RetrieveUpdateAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        # For normal operations, use the default queryset
        if self.action in ["restore", "hard_delete"]:
            return User.all_objects.all()
        return User.objects.all()

    def get_object(self):
        # Override to fetch from all_objects
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def _get_user_or_404(self, pk):
        try:
            user = User.all_objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404("User not found")

    @action(detail=False, methods=["get"], url_path="soft-delete")
    def soft_delete(self, request):
        deleted_users = User.deleted_objects.all()

        # Paginate the queryset of deleted instances
        page = self.paginate_queryset(deleted_users)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(deleted_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        user = self._get_user_or_404(pk)

        if user.is_deleted:
            user.restore()
            return Response(
                {"status": "user restored"}, status=status.HTTP_200_OK
            )
        return Response(
            {"status": "user is not deleted"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["delete"], url_path="hard-delete")
    def hard_delete(self, request, pk=None):
        user = self._get_user_or_404(pk)

        user.hard_delete()
        return Response(
            {"status": "user permanently deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PermissionViewSet(BaseModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
