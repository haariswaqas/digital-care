from rest_framework import serializers
from ..models import Consultation, Appointment
from .AppointmentSerializers import AppointmentSerializer


class ConsultationSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    appointment_id = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.all(),
        write_only=True,
        source="appointment"
    )

    class Meta:
        model = Consultation
        fields = [
            "id", "appointment", "appointment_id",
            "notes", "diagnosis", "started_at", "ended_at",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        """
        Only doctors should create consultations,
        each appointment should only have ONE consultation,
        and doctors can only create consultations for their own appointments.
        """
        request = self.context.get("request")
        user = request.user if request else None
        appointment = validated_data.get("appointment")

        # Ensure a consultation doesn’t already exist
        if hasattr(appointment, "consultation"):
            raise serializers.ValidationError("This appointment already has a consultation.")

        # Only doctors can create consultations
        if not (user and hasattr(user, "doctorprofile")):
            raise serializers.ValidationError("Only doctors can create consultations.")

        # Ensure the doctor is assigned to this appointment
        if appointment.doctor and appointment.doctor.user != user:
            raise serializers.ValidationError("You can only create consultations for your own appointments.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Allow doctors to update consultation notes, diagnosis, etc.
        """
        request = self.context.get("request")
        user = request.user if request else None

        if not (user and hasattr(user, "doctorprofile")):
            raise serializers.ValidationError("Only doctors can update consultations.")

        return super().update(instance, validated_data)
