from abc import ABC, abstractmethod

# Django
from django.views.generic import TemplateView

# Local
from .mixins import SuperUserPermissionMixin, AdminContextMixin

# A dictionary to store registered checks
registered_checks = {}


def register_check(check_class):
    """
    Decorator to register health check classes.
    """
    registered_checks[check_class.__name__] = check_class
    return check_class


class DataHealthCheck(ABC):
    """
    Base class for data health checks.
    """

    name = ""
    description = ""
    object_name = None

    @abstractmethod
    def check(self) -> list:
        """
        Return the objects that are failing the check.
        """
        pass

    def __init__(self):
        self.slug = self.get_slug()
        self.success = False
        self.error_message = None
        self.failing_objects = None
        self.has_fix = hasattr(self, "fix")

    def get_slug(self):
        return self.name.lower().replace(" ", "_")

    def perform_check(self):
        self.failing_objects = self.check()
        self.success = len(self.failing_objects) == 0

        if not self.success:
            self.error_message = self.get_error_message()

    def get_object_name(self) -> str:
        return self.object_name.lower() if self.object_name else "object"

    def get_error_message(self):
        object_name = self.get_object_name()
        object_string = (
            f"{object_name}s are"
            if len(self.failing_objects) > 1
            else f"{object_name} is"
        )
        return f"{len(self.failing_objects)} {object_string} failing the check."


class DataHealthChecksAdminView(SuperUserPermissionMixin, AdminContextMixin, TemplateView):
    template_name = "admin/data_health_checks/data_health_checks.html"

    def __init__(self):
        self.checks = [check_class() for check_class in registered_checks.values()]
        super().__init__()

    def get_context_data(self, **kwargs):
        context = {
            "checks": self.execute_checks(),
        }
        return super().get_context_data(**context)

    def execute_checks(self):
        for check in self.checks:
            check.perform_check()

        return self.checks

    def post(self, request, *args, **kwargs):
        slug = request.POST.get("slug")

        for check in self.checks:
            if check.slug == slug:
                if check.has_fix:
                    check.fix()
                    break
                raise ValueError("This check does not have a fix method.")

        return self.get(request, *args, **kwargs)
