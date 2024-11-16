# new and update models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    department = models.CharField(max_length=100)
    # Add any other fields you want

    def __str__(self):
        return self.username

class Incident(models.Model):
    # Keeping your existing choices
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    STATUS_CHOICES = [
        ('', 'Click to select Severity'),  # Placeholder
        ('REPORTED', 'Reported'),
        ('IN_PROGRESS', 'In Progress'),
        ('IN_REVIEW', 'In Review'),
        ('ESCALATED', 'Escalated'),
        ('RESOLVED', 'Resolved'),
    ]

    # Your existing fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    incident_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_incidents')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    incident_id = models.CharField(max_length=20, unique=True, editable=False, null=True)
    admin_notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.incident_id:
            last_incident = Incident.objects.order_by('-id').first()
            if last_incident:
                last_id = int(last_incident.incident_id[3:])
                self.incident_id = f"INC{last_id + 1:04d}"
            else:
                self.incident_id = "INC0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.incident_id}: {self.title}"

# New model for storing intelligent analysis results
class IncidentAnalysis(models.Model):
    # Link this analysis to a specific incident
    incident = models.OneToOneField(Incident, on_delete=models.CASCADE, related_name='analysis')
    
    # Store the AI's prediction confidence (e.g., 0.95 for 95% confident)
    ai_confidence = models.FloatField(
        help_text="How confident the AI is about its analysis (0-1)"
    )
    
    # Store any IP addresses found in the incident description
    detected_ips = models.JSONField(
        null=True, blank=True,
        help_text="IP addresses found in the incident description"
    )
    
    # Store any URLs found in the incident description
    detected_urls = models.JSONField(
        null=True, blank=True,
        help_text="URLs found in the incident description"
    )
    
    # Store any usernames or system names found
    detected_systems = models.JSONField(
        null=True, blank=True,
        help_text="Usernames or system names found in the description"
    )
    
    # AI-suggested recommendations for handling the incident
    ai_recommendations = models.JSONField(
        help_text="AI-generated recommendations for handling the incident"
    )
    
    # When this analysis was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When this analysis was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Incident Analyses"

    def __str__(self):
        return f"Analysis for {self.incident.incident_id}"

# Optional: Add a model for tracking similar incidents
class RelatedIncidents(models.Model):
    # The main incident
    primary_incident = models.ForeignKey(
        Incident, 
        on_delete=models.CASCADE,
        related_name='primary_relationships'
    )
    
    # An incident that might be related
    related_incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name='secondary_relationships'
    )
    
    # How similar these incidents are (0-1)
    similarity_score = models.FloatField(
        help_text="How similar these incidents are (0-1)"
    )
    
    # When this relationship was identified
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['primary_incident', 'related_incident']
        verbose_name_plural = "Related Incidents"

    def __str__(self):
        return f"{self.primary_incident.incident_id} ↔ {self.related_incident.incident_id}"

# New model for tracking incident history
class IncidentHistory(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20, choices=Incident.STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Incident Histories"

    def __str__(self):
        return f"History for {self.incident.incident_id} - {self.created_at}"




















    
# OLD MODELS.PY FILE
# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings
# from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     department = models.CharField(max_length=100)
#     # Add any other fields you want

#     def __str__(self):
#         return self.username

# # Create your models here.
# class Incident(models.Model):
#     SEVERITY_CHOICES = [
#         ('LOW', 'Low'),
#         ('MEDIUM', 'Medium'),
#         ('HIGH', 'High'),
#     ]
#     STATUS_CHOICES = [
#         ('REPORTED', 'Reported'),
#         ('IN_PROGRESS', 'In Progress'),
#         ('IN_REVIEW', 'In Review'),
#         ('ESCALATED', 'Escalated'),
#         ('RESOLVED', 'Resolved'),
#     ]

#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     incident_type = models.CharField(max_length=100)
#     severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')
#     reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_incidents')
#     assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     incident_id = models.CharField(max_length=20, unique=True, editable=False, null=True)

#     def save(self, *args, **kwargs):
#         if not self.incident_id:
#             last_incident = Incident.objects.order_by('-id').first()
#             if last_incident:
#                 last_id = int(last_incident.incident_id[3:])
#                 self.incident_id = f"INC{last_id + 1:04d}"
#             else:
#                 self.incident_id = "INC0001"
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.incident_id}: {self.title}"
    
