from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from ..models import StudentProfile, VisitorProfile, AdultProfile
from ..serializers import (
    StudentProfileSerializer,
    VisitorProfileSerializer,
    AdultProfileSerializer,
)


# Base class for CRUD on user-owned profiles
class BaseProfileView(
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    model_class = None
    role = None  # To be set in each subclass

    def get_object(self):
        if self.request.user.role != self.role:
            raise PermissionDenied({"detail": "Access Denied."})
        return get_object_or_404(self.model_class, user=self.request.user)

    def get(self, request, *args, **kwargs):
        """Retrieve logged-in user's profile"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create profile if not already existing"""
        if self.model_class.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "Profile already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update logged-in user's profile"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete logged-in user's profile"""
        return self.destroy(request, *args, **kwargs)


class StudentProfileView(BaseProfileView):
    serializer_class = StudentProfileSerializer
    model_class = StudentProfile
    role = "student"


class VisitorProfileView(BaseProfileView):
    serializer_class = VisitorProfileSerializer
    model_class = VisitorProfile
    role = "visitor"


class AdultProfileView(BaseProfileView):
    serializer_class = AdultProfileSerializer
    model_class = AdultProfile
    role = "adult"
