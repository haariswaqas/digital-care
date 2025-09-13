# api/models/user.py

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Simplified custom User model for MVP."""
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    ADMIN = 'admin'
    FACILITY_ADMIN = 'facility_admin'
    STUDENT = 'student'
    ADULT = 'adult'
    VISITOR = 'visitor'
    DOCTOR = 'doctor'
    
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        
        (FACILITY_ADMIN, 'Facility Admin'),
        (STUDENT, 'Student'),
        (ADULT, 'Adult'),
        (VISITOR, 'Visitor'), 
        (DOCTOR, 'Doctor')
        
        
    ]
    ACTIVE = 'active'
    BANNED = 'banned'
    SUSPENDED = 'suspended'
    ON_LEAVE = 'on_leave'
    PENDING = 'pending'
    
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (BANNED, 'Banned'),
        (SUSPENDED, 'Suspended'),
        (ON_LEAVE, 'On Leave'),
        (PENDING, 'Pending')

    ]
    

    phone_number = models.CharField(max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')
            )
        ],
        unique=True
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=STUDENT)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return f"#{self.id} ({self.role}). {self.username} - {self.email}"
