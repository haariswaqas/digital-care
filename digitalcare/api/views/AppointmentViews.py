# api/views/appointment_views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Appointment
from ..serializers import AppointmentSerializer

from ..permissions import AppointmentPermissions

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, AppointmentPermissions]

    def perform_create(self, serializer):
        # Patient automatically assigned
        serializer.save(patient=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == "admin":
            return Appointment.objects.all()
        elif user.role == "facility_admin":
            return Appointment.objects.filter(facility__admin=user)
        elif user.role == "doctor":
            return Appointment.objects.filter(doctor__user=user)
        else:
            return Appointment.objects.filter(patient=user)

    # Doctor actions: confirm or cancel
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, AppointmentPermissions])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        if appointment.status != Appointment.PENDING:
            return Response({"detail": "Only pending appointments can be confirmed."}, status=400)
        appointment.status = Appointment.CONFIRMED
        appointment.save()
        return Response({"status": "confirmed"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, AppointmentPermissions])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if appointment.status not in [Appointment.PENDING, Appointment.CONFIRMED]:
            return Response({"detail": "Only pending or confirmed appointments can be cancelled."}, status=400)
        appointment.status = Appointment.CANCELLED
        appointment.save()
        return Response({"status": "cancelled"})
