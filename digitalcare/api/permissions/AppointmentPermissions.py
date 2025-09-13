# api/permissions/appointment_permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class AppointmentPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Patients can create appointments
        if view.action == "create" and user.role in ["student", "adult", "visitor"]:
            return True

        # Doctors can confirm/cancel appointments (but not create)
        if view.action in ["confirm", "cancel"] and user.role == "doctor":
            return True

        # Facility Admin / Admin / Superuser can do everything
        if user.role in ["admin", "facility_admin"] or user.is_superuser:
            return True

        # Read access (list/retrieve) for doctors & patients to their own
        if view.action in ["list", "retrieve"]:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role == "admin":
            return True
        if user.role == "facility_admin" and obj.facility and obj.facility.admin == user:
            return True
        if user.role == "doctor" and obj.doctor and obj.doctor.user == user:
            return True
        if obj.patient == user:
            return True
        return False

