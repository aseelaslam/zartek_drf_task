from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
# Create your models here.



class User(AbstractUser):
    pass
    
   
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='ride_users'  
    )

    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='ride_users_permissions'  
    )


from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_requested')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='rides_accepted')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} - {self.rider.username}"
