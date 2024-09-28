from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    department = models.CharField(max_length=100)
    # Add any other fields you want

    def __str__(self):
        return self.username

# Create your models here.
class Incident(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('IN_PROGRESS', 'In Progress'),
        ('IN_REVIEW', 'In Review'),
        ('ESCALATED', 'Escalated'),
        ('RESOLVED', 'Resolved'),
    ]

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
    
