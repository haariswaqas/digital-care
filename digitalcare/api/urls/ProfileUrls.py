from django.urls import path
from api.views import (
    StudentProfileView,
    VisitorProfileView,
    AdultProfileView,
)

urlpatterns = [
    path("student/profile/", StudentProfileView.as_view(), name="student-profile"),
    path("visitor/profile/", VisitorProfileView.as_view(), name="visitor-profile"),
    path("adult/profile/", AdultProfileView.as_view(), name="adult-profile"),
]
