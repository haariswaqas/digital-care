# api/permissions/symptom_permissions.py
from rest_framework.permissions import BasePermission

class SymptomPermission(BasePermission):
    """
    Permission class for Symptom model:
    - Patients can create symptoms only for their own appointments.
    - Doctors can manage symptoms for appointments they are assigned to.
    - Facility Admin / Admin / Superuser have full access.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Doctors can create/update/delete
        if view.action in ["create", "update", "partial_update", "destroy"] and user.role == "doctor":
            return True

        # Patients can create (for their own appointments) and list/retrieve
        if view.action in ["create", "list", "retrieve"] and user.role in ["student", "adult", "visitor"]:
            return True

        # Facility Admin / Admin / Superuser can do everything
        if user.role in ["admin", "facility_admin"] or user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser or user.role == "admin":
            return True

        if user.role == "facility_admin" and obj.appointment.facility and obj.appointment.facility.admin == user:
            return True

        # Doctors can manage symptoms only for their appointments
        if user.role == "doctor" and obj.appointment.doctor and obj.appointment.doctor.user == user:
            return True

        # Patients can only manage or view symptoms of their own appointments
        if user.role in ["student", "adult", "visitor"] and obj.appointment.patient == user:
            # Allow create, list, retrieve
            return view.action in ["list", "retrieve", "create"]

        return False
