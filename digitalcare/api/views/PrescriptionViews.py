# api/views/prescription_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Prescription
from ..serializers import PrescriptionSerializer
from ..permissions import PrescriptionPermissions


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, PrescriptionPermissions]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == "admin":
            return Prescription.objects.all()
        elif user.role == "facility_admin":
            return Prescription.objects.filter(
                consultation__appointment__facility__admin=user
            )
        elif user.role == "doctor":
            return Prescription.objects.filter(
                consultation__appointment__doctor__user=user
            )
        else:
            # patient
            return Prescription.objects.filter(
                consultation__appointment__patient=user
            )

    def perform_create(self, serializer):
        consultation = serializer.validated_data["consultation"]
        user = self.request.user

        # enforce: only doctor of the consultation’s appointment can create
        if consultation.appointment.doctor is None or consultation.appointment.doctor.user != user:
            raise PermissionError("You are not allowed to add a prescription for this consultation.")

        serializer.save()
