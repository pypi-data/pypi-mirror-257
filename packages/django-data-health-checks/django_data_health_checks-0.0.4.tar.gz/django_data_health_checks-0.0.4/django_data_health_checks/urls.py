from django.urls import path

from .data_health_check import DataHealthChecksAdminView

app_name = "django_data_health_checks"
urlpatterns = [
    path("data-health-checks/", DataHealthChecksAdminView.as_view(), name="data-health-checks"),
]
