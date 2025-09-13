from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Consultation
from ..serializers import ConsultationSerializer
from ..permissions import ConsultationPermissions


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated, ConsultationPermissions]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == "admin":
            return Consultation.objects.all()
        elif user.role == "facility_admin":
            return Consultation.objects.filter(appointment__facility__admin=user)
        elif user.role == "doctor":
            return Consultation.objects.filter(appointment__doctor__user=user)
        else:
            # Patient
            return Consultation.objects.filter(appointment__patient=user)
