from rest_framework.permissions import BasePermission


class IsSelfEnrollment(BasePermission):
    """Ensures users only access their own enrollment collections."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user_id == request.user.id
