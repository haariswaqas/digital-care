from django.contrib import admin
from .models import User, Otp, AdultProfile, VisitorProfile, StudentProfile, DoctorProfile, HealthCard, Facility, Notification, Appointment, Consultation, Prescription, Symptom
# Register your models here.
reg = admin.site.register

reg(User)
reg(Otp)

reg(AdultProfile)
reg(VisitorProfile)
reg(StudentProfile)

reg(HealthCard)

reg(Facility)
reg(Appointment)
reg(Consultation)
reg(DoctorProfile)
reg(Notification)
reg(Prescription)
reg(Symptom)

