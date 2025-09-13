# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import SymptomViewSet

router = DefaultRouter()
router.register(r'symptoms', SymptomViewSet, basename='symptom')  # register symptom endpoint

urlpatterns = [
    path('', include(router.urls)),
]
