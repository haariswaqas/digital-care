from django.contrib import admin
from .models import User, Otp, AdultProfile, VisitorProfile, StudentProfile, HealthCard
# Register your models here.
reg = admin.site.register

reg(User)
reg(Otp)

reg(AdultProfile)
reg(VisitorProfile)
reg(StudentProfile)

reg(HealthCard)