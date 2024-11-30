from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('installation', 'Installation'),
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('billing', 'Billing Issue'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    attached_files = models.FileField(upload_to='service_requests/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request #{self.id} - {self.service_type}"

    def resolve(self):
        self.status = 'resolved'
        self.resolved_at = models.DateTimeField(auto_now=True)
        self.save()


