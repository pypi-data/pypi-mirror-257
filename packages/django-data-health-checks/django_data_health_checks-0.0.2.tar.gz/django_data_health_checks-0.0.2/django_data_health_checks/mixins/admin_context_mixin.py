# Django
from django.contrib.admin.sites import site


class AdminContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**site.each_context(self.request))
        return super().get_context_data(**context)
