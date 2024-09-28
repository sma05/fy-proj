from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'incident_type', 'severity']

# creation of new users to the system
class CustomUserCreationForm(UserCreationForm):
    usable_password = None
    email = forms.EmailField(required=True)
    department = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "department", "password1", "password2")

# this form is responsible for gathering incident report from user
class IncidentReportForm(forms.ModelForm):
    INCIDENT_TYPES = [
        ('unauthorized_access', 'Unauthorized Access Attempt'),
        ('suspicious_network', 'Suspicious Network Activity'),
        ('data_breach', 'Data Breach Attempt'),
        ('phishing', 'Phishing Attempt'),
        ('malware', 'Malware Infection'),
    ]

    incident_type = forms.ChoiceField(choices=INCIDENT_TYPES)

    class Meta:
        model = Incident
        fields = ['title', 'description', 'incident_type', 'severity']



# admin custome admin dashboard

# forms.py

from django import forms

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}))