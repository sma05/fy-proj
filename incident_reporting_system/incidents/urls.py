from django.urls import path
from . import views


# below  urlpatterns own the first two imports
urlpatterns =[
    # path('', views.home, name='home'),
    path('report/', views.report_incident, name='report_incident'),
    path('list/', views.incident_list, name='incident_list'),
    path('report/submit/', views.submit_incident, name='submit_incident'),
    path('incidents/detail/<str:incident_id>/', views.incident_detail, name='incident_detail'),

    # urlpatterns for customized admin dashboard
    path('custom-admin/login/', views.custom_admin_login, name='custom_admin_login'),
    path('custom-admin/dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('custom-admin/users/', views.custom_admin_user_management, name='custom_admin_user_management'),
    path('custom-admin/incidents/', views.custom_admin_incident_management, name='custom_admin_incident_management'),
    path('report/edit/<str:incident_id>/', views.edit_incident, name='edit_incident'),
]




# below  url  patterns own the 2nd stand-alone import

urlpatterns += [
    path('custom-admin/incidents/update/<str:incident_id>/', views.admin_update_incident, name='admin_update_incident'),
    path('my-incidents/', views.user_incident_tracking, name='user_incident_tracking'),
]




# below  url  patterns own the 2nd stand-alone import
