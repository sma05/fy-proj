from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Incident, CustomUser
from .forms import IncidentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm, IncidentReportForm
from .models import Incident, CustomUser

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .forms import AdminLoginForm

# admin/IT PERSONNEL's view login and all of that

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def custom_admin_dashboard(request):
    total_incidents = Incident.objects.count()
    open_incidents = Incident.objects.filter(status__in=['REPORTED', 'IN_PROGRESS']).count()
    resolved_incidents = Incident.objects.filter(status='RESOLVED').count()
    incidents_by_type = Incident.objects.values('incident_type').annotate(count=Count('id'))
    recent_incidents = Incident.objects.order_by('-created_at')[:5]
    user_activity = CustomUser.objects.annotate(incident_count=Count('reported_incidents')).order_by('-incident_count')[:5]
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    incidents_over_time = Incident.objects.filter(created_at__gte=thirty_days_ago).values('created_at__date').annotate(count=Count('id'))

    context = {
        'total_incidents': total_incidents,
        'open_incidents': open_incidents,
        'resolved_incidents': resolved_incidents,
        'incidents_by_type': incidents_by_type,
        'recent_incidents': recent_incidents,
        'user_activity': user_activity,
        'incidents_over_time': list(incidents_over_time),
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin)
def custom_admin_user_management(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/user_management.html', {'users': users})

@user_passes_test(is_admin)
def custom_admin_incident_management(request):
    incidents = Incident.objects.all().order_by('-created_at')
    return render(request, 'admin/incident_management.html', {'incidents': incidents})

def custom_admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('custom_admin_dashboard')
            else:
                form.add_error(None, "Invalid username or password, or insufficient permissions.")
    else:
        form = AdminLoginForm()
    return render(request, 'admin/login.html', {'form': form})


# admin IT personel ends




# Create your views here.


# flash message for unathourized user/restriction from protected views
def login_required_with_message(message):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, message)
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator



# register a user
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

#new user registration to disable that thing I want to disable on the registration form
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user yet
            user.set_unusable_password()  # This will set the password as unusable
            user.save()  # Now save the user instance
            login(request, user)  # Log in the user
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})








# @login_required
def home(request):
    return render(request, 'incidents/home.html')

@login_required_with_message("Please login to report an incident")
def report_incident(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()
            messages.success(request, f"Incident {incident.incident_id} has been reported successfully.")
            return redirect('incident_list')
    else:
        form = IncidentReportForm()
    return render(request, 'incidents/report_incident.html', {'form': form})

@login_required_with_message("Please login to report an incident")
def incident_list(request):
    incidents = Incident.objects.filter(reported_by=request.user).order_by('-created_at')
    return render(request, 'incidents/incident_list.html', {'incidents': incidents})


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

















