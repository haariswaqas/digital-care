# api/permissions/consultation_permissions.py
from rest_framework.permissions import BasePermission


class ConsultationPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Only doctors can create consultations
        if view.action == "create" and user.role == "doctor":
            return True

        # Doctors can update consultations
        if view.action in ["update", "partial_update"] and user.role == "doctor":
            return True

        # Facility Admin / Admin / Superuser can do everything
        if user.role in ["admin", "facility_admin"] or user.is_superuser:
            return True

        # Patients & doctors can list/retrieve consultations they’re involved in
        if view.action in ["list", "retrieve"]:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser or user.role == "admin":
            return True
        if user.role == "facility_admin" and obj.appointment.facility and obj.appointment.facility.admin == user:
            return True
        if user.role == "doctor" and obj.appointment.doctor and obj.appointment.doctor.user == user:
            return True
        if obj.appointment.patient == user:
            return True
        return False
