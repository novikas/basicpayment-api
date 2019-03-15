from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.owner.id == request.user.pk
