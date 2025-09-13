from rest_framework import permissions

class IsFacilityAdminOfOwnFacility(permissions.BasePermission):
    """
    Allow facility admins to CRUD only their own facility data.
    """

    def has_object_permission(self, request, view, obj):
        # Superusers/admins can do anything
        if request.user.is_superuser or request.user.role == 'admin':
            return True

        # Facility admins can only manage their own facility
        if request.user.role == 'facility_admin':
            return obj.admin == request.user

        # Default deny
        return False
