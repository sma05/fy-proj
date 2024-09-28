from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Incident
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'department', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Incident)



# Create a simple view for the dashboard
def admin_dashboard(request):
    # Return a simple template response, you can expand this to your dashboard needs
    context = {}
    return TemplateResponse(request, 'incidents/admin_dashboard.html', context)

# Customizing admin URLs
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='dashboard'),
        ]
        return custom_urls + urls

# Instantiate the CustomAdminSite
custom_admin_site = CustomAdminSite(name='customadmin')



