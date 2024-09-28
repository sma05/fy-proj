"""
URL configuration for incident_reporting_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from incidents.views import home, register, custom_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('incidents/', include('incidents.urls')),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, next_page='/'), name='login'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout'),
]