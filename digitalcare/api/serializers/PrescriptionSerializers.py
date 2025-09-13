# api/serializers/prescription_serializer.py
from rest_framework import serializers
from ..models import Prescription
from .ConsultationSerializers import ConsultationSerializer


class PrescriptionSerializer(serializers.ModelSerializer):
    consultation = ConsultationSerializer(read_only=True)
    consultation_id = serializers.PrimaryKeyRelatedField(
        queryset=Prescription._meta.get_field("consultation").related_model.objects.all(),
        write_only=True,
        source="consultation"
    )

    class Meta:
        model = Prescription
        fields = [
            "id", "consultation", "consultation_id",
            "medicine_name", "dosage", "frequency", "duration", "instructions",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]
