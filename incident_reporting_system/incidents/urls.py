from django.urls import path
from . import views


# below  urlpatterns own the first two imports
urlpatterns =[
    # path('', views.home, name='home'),
    path('report/', views.report_incident, name='report_incident'),
    path('list/', views.incident_list, name='incident_list'),

    # urlpatterns for customized admin dashboard
    path('custom-admin/login/', views.custom_admin_login, name='custom_admin_login'),
    path('custom-admin/dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('custom-admin/users/', views.custom_admin_user_management, name='custom_admin_user_management'),
    path('custom-admin/incidents/', views.custom_admin_incident_management, name='custom_admin_incident_management'),
]


# below  url  patterns own the 2nd stand-alone import
