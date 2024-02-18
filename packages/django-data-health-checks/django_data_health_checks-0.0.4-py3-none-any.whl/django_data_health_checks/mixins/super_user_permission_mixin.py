# Django
from django.contrib.auth.mixins import PermissionRequiredMixin


class SuperUserPermissionMixin(PermissionRequiredMixin):
    def has_permission(self):
        user = self.request.user
        return user.is_superuser
