# api/serializers/symptom_serializer.py
from rest_framework import serializers
from ..models import Symptom, Appointment
from .AppointmentSerializers import AppointmentSerializer

class SymptomSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    appointment_id = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.all(),
        write_only=True,
        source="appointment"
    )
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Symptom
        fields = [
            "id", "appointment", "appointment_id",
            "description", "image",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        """
        Patients can create symptoms linked to their appointments.
        """
        request = self.context.get("request")
        user = request.user if request else None
        appointment = validated_data.get("appointment")

        # Ensure only the patient of this appointment can create a symptom
        if user and appointment.patient != user:
            raise serializers.ValidationError("You can only add symptoms to your own appointments.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Allow patients to update description or image.
        """
        request = self.context.get("request")
        user = request.user if request else None

        if user and instance.appointment.patient != user:
            raise serializers.ValidationError("You can only update your own symptoms.")

        return super().update(instance, validated_data)
