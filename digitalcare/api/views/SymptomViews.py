# api/views/symptom_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Symptom
from ..serializers import SymptomSerializer
from ..permissions import SymptomPermission

class SymptomViewSet(viewsets.ModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [IsAuthenticated, SymptomPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == "admin":
            return Symptom.objects.all()
        elif user.role == "facility_admin":
            return Symptom.objects.filter(appointment__facility__admin=user)
        elif user.role == "doctor":
            return Symptom.objects.filter(appointment__doctor__user=user)
        else:
            # Patient
            return Symptom.objects.filter(appointment__patient=user)

    def perform_create(self, serializer):
        """
        Ensure the patient is creating a symptom for their own appointment.
        """
        serializer.save()
