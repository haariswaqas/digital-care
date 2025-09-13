from rest_framework import serializers
from ..models import Appointment, DoctorProfile

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id", "patient", "doctor", "facility", "appointment_type",
            "scheduled_at", "duration_minutes", "reason", "status",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "facility", "status", "created_at", "updated_at", "patient"]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        validated_data["patient"] = user   # logged-in user is the patient

        doctor = validated_data.get("doctor")
        if not doctor:
            raise serializers.ValidationError("Doctor must be specified.")

        # Get the doctor's facilities
        clinics = doctor.clinics.all()

        if not clinics.exists():
            raise serializers.ValidationError("This doctor is not assigned to any facility.")

        if clinics.count() == 1:
            validated_data["facility"] = clinics.first()
        else:
            # If multiple clinics exist, require patient to specify via request
            facility_id = request.data.get("facility_id")
            if not facility_id:
                # Collect the IDs of clinics
                clinic_ids = list(clinics.values_list("id", flat=True))
                clinic_names = list(clinics.values_list("name", flat=True))
                raise serializers.ValidationError(
                    f"This doctor works at multiple facilities. Please specify 'facility_id'. "
                    f"Valid facility IDs: {clinic_ids} ==> {clinic_names}"
                )
            try:
                facility = clinics.get(id=facility_id)
                validated_data["facility"] = facility
            except clinics.model.DoesNotExist:
                raise serializers.ValidationError(
                    "Selected facility is not valid for this doctor."
                )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        # Prevent patients from manually updating status
        if user and user.role in ["student", "adult", "visitor"] and "status" in validated_data:
            validated_data.pop("status")

        return super().update(instance, validated_data)
