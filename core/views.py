from django.views.generic import TemplateView

from .permissions import AdminSiteMixin

class Dashboard(AdminSiteMixin, TemplateView):
    permission_required = ['core']
    template_name = "core/index.html"
    content_title = "Dashboard"