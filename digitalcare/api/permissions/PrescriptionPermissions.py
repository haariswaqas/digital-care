# api/permissions/prescription_permissions.py
from rest_framework.permissions import BasePermission


class PrescriptionPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Doctors can create/update/delete
        if view.action in ["create", "update", "partial_update", "destroy"] and user.role == "doctor":
            return True

        # Facility Admin / Admin / Superuser can do everything
        if user.role in ["admin", "facility_admin"] or user.is_superuser:
            return True

        # Patients and doctors can list/retrieve
        if view.action in ["list", "retrieve"]:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser or user.role == "admin":
            return True
        if user.role == "facility_admin" and obj.consultation.appointment.facility and obj.consultation.appointment.facility.admin == user:
            return True
        if user.role == "doctor" and obj.consultation.appointment.doctor and obj.consultation.appointment.doctor.user == user:
            return True
        if user.role in ["student", "adult", "visitor"] and obj.consultation.appointment.patient == user:
            # patients can ONLY view (list/retrieve), not modify
            return view.action in ["list", "retrieve"]
        return False
