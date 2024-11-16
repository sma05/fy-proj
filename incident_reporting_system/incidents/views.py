from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Incident, CustomUser, IncidentAnalysis, RelatedIncidents, IncidentHistory
from .forms import IncidentForm, CustomUserCreationForm, IncidentReportForm, AdminLoginForm, AdminIncidentUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .incident_analyzer import IncidentAnalyzer

# IMPORTS FOR THE AI FEATURES
from .incident_analyzer import IncidentAnalyzer
from .models import Incident, IncidentAnalysis, RelatedIncidents


# IMPORTS FOR THE NEW CUSTOME_ADMIN_DASHBOARD VIEW
from django.db.models import Count, Avg
from django.db.models.functions import TruncDay

# admin/IT PERSONNEL's view login and all of that

def is_admin(user):
    return user.is_authenticated and user.is_staff


# NEW CUSTOME_ADMIN_DASHBOARD VIEW THAT WORK WITH THE LATEST AI MODEL IN THE MODELS.PY FILE AND THE INCIDENT_ANALYZER FILE
# Updated admin dashboard view to work with our new models

from django.db.models import Count, Avg
from django.db.models.functions import TruncDay

@user_passes_test(is_admin)
def custom_admin_dashboard(request):
    # Get basic incident stats
    total_incidents = Incident.objects.count()
    open_incidents = Incident.objects.filter(status__in=['REPORTED', 'IN_PROGRESS']).count()
    resolved_incidents = Incident.objects.filter(status='RESOLVED').count()
    
    # Get AI analysis statistics
    incidents_by_type = Incident.objects.values('incident_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    severity_distribution = Incident.objects.values('severity').annotate(
        count=Count('id')
    ).order_by('severity')
    
    # Get average AI confidence by incident type
    avg_confidence_by_type = IncidentAnalysis.objects.values(
        'incident__incident_type'  # Note we're using incident__incident_type
    ).annotate(
        avg_confidence=Avg('ai_confidence')
    ).order_by('-avg_confidence')
    
    # Get recent high severity incidents
    recent_high_severity = Incident.objects.filter(
        severity='HIGH'
    ).select_related('analysis').order_by('-created_at')[:5]
    
    # Get incidents over time
    thirty_days_ago = timezone.now() - timedelta(days=30)
    incidents_over_time = Incident.objects.filter(
        created_at__gte=thirty_days_ago
    ).values('created_at__date').annotate(count=Count('id'))
    
    context = {
        'total_incidents': total_incidents,
        'open_incidents': open_incidents,
        'resolved_incidents': resolved_incidents,
        'incidents_by_type': incidents_by_type,
        'severity_distribution': severity_distribution,
        'avg_confidence_by_type': avg_confidence_by_type,
        'recent_high_severity': recent_high_severity,
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

@user_passes_test(is_admin)
def admin_update_incident(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id)
    if request.method == 'POST':
        form = AdminIncidentUpdateForm(request.POST, instance=incident)
        if form.is_valid():
            updated_incident = form.save()
            
            # Create a new IncidentHistory entry
            IncidentHistory.objects.create(
                incident=updated_incident,
                status=updated_incident.status,
                notes=updated_incident.admin_notes,
                updated_by=request.user
            )
            
            # Prepare email content
            email_subject = f'Update on Incident {incident.incident_id}'
            email_body = f"""
Your reported incident has been updated.

New status: {updated_incident.get_status_display()}

Admin notes:
{updated_incident.admin_notes}

Please log in to your account for more details.
"""
            
            # Send email to the user who reported the incident
            send_mail(
                email_subject,
                email_body,
                'noreply@example.com',
                [updated_incident.reported_by.email],
                fail_silently=False,
            )
            
            messages.success(request, f'Incident {incident.incident_id} has been updated and the user has been notified.')
            return redirect('custom_admin_incident_management')
    else:
        form = AdminIncidentUpdateForm(instance=incident)
    
    return render(request, 'admin/update_incident.html', {'form': form, 'incident': incident})

# Add this new view for users to track their incidents
@login_required
def user_incident_tracking(request):
    user_incidents = Incident.objects.filter(reported_by=request.user).order_by('-created_at')
    return render(request, 'incidents/user_incident_tracking.html', {'incidents': user_incidents})

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


    # NEW CUSTOME_ADMIN_DASHBOARD VIEW ENDS HERE











# OLD CUSTOME_ADMIN_DASHBOARD VIEW
# @user_passes_test(is_admin)
# def custom_admin_dashboard(request):
#     total_incidents = Incident.objects.count()
#     open_incidents = Incident.objects.filter(status__in=['REPORTED', 'IN_PROGRESS']).count()
#     resolved_incidents = Incident.objects.filter(status='RESOLVED').count()
#     incidents_by_type = Incident.objects.values('incident_type').annotate(count=Count('id'))
#     recent_incidents = Incident.objects.order_by('-created_at')[:5]
#     user_activity = CustomUser.objects.annotate(incident_count=Count('reported_incidents')).order_by('-incident_count')[:5]
    
#     thirty_days_ago = timezone.now() - timedelta(days=30)
#     incidents_over_time = Incident.objects.filter(created_at__gte=thirty_days_ago).values('created_at__date').annotate(count=Count('id'))

#     context = {
#         'total_incidents': total_incidents,
#         'open_incidents': open_incidents,
#         'resolved_incidents': resolved_incidents,
#         'incidents_by_type': incidents_by_type,
#         'recent_incidents': recent_incidents,
#         'user_activity': user_activity,
#         'incidents_over_time': list(incidents_over_time),
#     }
#     return render(request, 'admin/dashboard.html', context)

# @user_passes_test(is_admin)
# def custom_admin_user_management(request):
#     users = CustomUser.objects.all()
#     return render(request, 'admin/user_management.html', {'users': users})

# @user_passes_test(is_admin)
# def custom_admin_incident_management(request):
#     incidents = Incident.objects.all().order_by('-created_at')
#     return render(request, 'admin/incident_management.html', {'incidents': incidents})

# def custom_admin_login(request):
#     if request.method == 'POST':
#         form = AdminLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None and user.is_staff:
#                 login(request, user)
#                 return redirect('custom_admin_dashboard')
#             else:
#                 form.add_error(None, "Invalid username or password, or insufficient permissions.")
#     else:
#         form = AdminLoginForm()
#     return render(request, 'admin/login.html', {'form': form})


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
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            
            # Analyze the incident using the Hugging Face model
            analyzer = IncidentAnalyzer()
            analysis_results = analyzer.analyze_incident(
                title=incident.title,
                description=incident.description,
                incident_type=incident.incident_type
            )
            
            summary = analysis_results['summary']
            
            return render(request, 'incidents/review_incident.html', {
                'form': form,
                'summary': summary,
                'incident': incident
            })
    else:
        form = IncidentForm()
    
    return render(request, 'incidents/report_incident.html', {'form': form})

@login_required_with_message("Please login to report an incident")
def submit_incident(request):
    if request.method == 'POST':
        incident_id = request.POST.get('incident_id')  # Get the incident ID from the form
        
        # Attempt to retrieve the incident; if not found, return a 404 error
        incident = get_object_or_404(Incident, incident_id=incident_id)
        
        # Save the incident to the database
        incident.save()  # Finalize the incident submission
        
        # Flash message to indicate success
        messages.success(request, f"The incident {incident.incident_id} has been reported successfully.")
        return redirect('incident_list')  # Redirect to the view incidents page
    
    return redirect('report_incident')  # Redirect back to the report page if not a POST request

@login_required_with_message("Please login to report an incident")
def incident_list(request):
    incidents = Incident.objects.filter(reported_by=request.user).order_by('-created_at')
    return render(request, 'incidents/incident_list.html', {'incidents': incidents})


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')



# ARITIFICIAL INTELLIGENCE VIEW

# THE CODE BELOW EXTENDS FROM THE THE INCIDENT_ANALYZER.PY FILE CREATED

# Add to your views.py


@login_required
def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id)
    
    # Ensure the user has permission to view this incident
    if incident.reported_by != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this incident.")
        return redirect('incident_list')
    
    try:
        analysis = incident.analysis
    except IncidentAnalysis.DoesNotExist:
        analysis = None
    
    related_incidents = RelatedIncidents.objects.filter(primary_incident=incident)
    incident_history = IncidentHistory.objects.filter(incident=incident)
    
    context = {
        'incident': incident,
        'analysis': analysis,
        'related_incidents': related_incidents,
        'incident_history': incident_history,
    }
    
    return render(request, 'incidents/incident_detail.html', context)

@login_required
def edit_incident(request, incident_id):
    incident = get_object_or_404(Incident, incident_id=incident_id)
    
    if request.method == 'POST':
        form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            messages.success(request, "The incident has been updated successfully.")
            return redirect('incident_list')  # Redirect to the view incidents page
    else:
        form = IncidentForm(instance=incident)
    
    return render(request, 'incidents/report_incident.html', {'form': form})













