from django.contrib.admin import AdminSite
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from functools import wraps

class AdminSiteMixin(LoginRequiredMixin, PermissionRequiredMixin):
    content_title: str = None
    content_sub_title: str = None

    def admin_site(self):
        admin_site = {
            'is_nav_sidebar_enabled': AdminSite.enable_nav_sidebar,
            'is_popup': False,
            'site_title': AdminSite.site_title,
            'has_permission': AdminSite.has_permission(AdminSite, self.request)
        }
        return admin_site
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        admin = self.admin_site()
        for k, v in admin.items():
            context[k] = v
        
        context['title'] = self.get_content_title()
        context['subtitle'] = self.get_content_subtitle()
        return context
    
    def get_content_title(self):
        return self.content_title
    
    def get_content_subtitle(self):
        return self.content_sub_title

class UserSiteMixin(LoginRequiredMixin):
    content_title: str = None
    content_sub_title: str = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.get_content_title()
        context['subtitle'] = self.get_content_subtitle()
        return context
    
    def get_content_title(self):
        return self.content_title
    
    def get_content_subtitle(self):
        return self.content_sub_title
    
    def get_account_role(self, request) -> bool:
        if hasattr(request, "role"): return True
        if request.user.is_superuser: return True
        return False

    def handle_no_permission(self):
        from urllib.parse import urlparse
        from django.contrib import messages
        from django.contrib.auth.views import redirect_to_login
        from django.shortcuts import resolve_url

        path = self.request.build_absolute_uri()
        resolved_login_uri = resolve_url(self.get_login_url())
        messages.add_message(
            self.request,
            messages.ERROR,
            "Anda tidak diizinkan masuk halaman ini "
            "karena tidak memiliki izin akses. "
            "Jika ini kesalahan, silahkan hubungi admin!"
        )

        login_scheme, login_netloc = urlparse(resolved_login_uri)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]

        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        
        return redirect_to_login(
            path,
            resolved_login_uri,
            self.get_redirect_field_name()
        )
    
    def dispatch(self, request, *args, **kwargs):
        if not self.get_account_role(request):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def required_ajax(f):
    @wraps(f)
    def _wrap(request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponseForbidden()
        return f(request, *args, **kwargs)
    return _wrap