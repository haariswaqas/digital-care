from rest_framework import serializers
from ..models import Facility, DoctorProfile

class DoctorBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["id", "first_name", "last_name", "specialty"]


class FacilitySerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)  # show username/email of the admin
    doctors = DoctorBasicSerializer(many=True, read_only=True, source='doctors')

    class Meta:
        model = Facility
        fields = [
            "id",
            "name",
            "facility_type",
            "address",
            "phone",
            "latitude",
            "longitude",
            "is_partner",
            "created_at",
            "updated_at",
            "admin", 'doctors'
        ]
        read_only_fields = ["id", "created_at", "updated_at", "admin", "doctors"]

    def create(self, validated_data):
        """
        Ensure the logged-in user is set as admin automatically.
        """
        user = self.context["request"].user
        facility = Facility.objects.create(admin=user, **validated_data)
        return facility

    def update(self, instance, validated_data):
        """
        Prevent facility admin from changing the admin user.
        """
        validated_data.pop("admin", None)
        return super().update(instance, validated_data)
